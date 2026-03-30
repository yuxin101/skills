#!/usr/bin/env python3
"""
claw-social-feed: 抓取 → 过滤 → 打标签 → 存入 Obsidian
依赖: bb-browser (via --openclaw), Python 3.8+
用法: python3 fetch_save.py [--config path/to/config.yaml]
"""
import json
import re
import os
import sys
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── 路径设置 ──────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
DEFAULT_CONFIG = SCRIPT_DIR.parent / "config.yaml"
DEFAULT_STATE = SCRIPT_DIR.parent / ".claw-social-feed-state.json"


# ── CLI 参数 ──────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(description="claw-social-feed: fetch & save to Obsidian")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="配置文件路径")
    parser.add_argument("--dry-run", action="store_true", help="仅模拟，不写入文件")
    parser.add_argument("--verbose", action="store_true", help="输出详细信息")
    return parser.parse_args()


# ── 配置加载 ──────────────────────────────────────
def load_config(path: str) -> dict:
    import yaml
    with open(path) as f:
        return yaml.safe_load(f)


def check_accounts(config: dict) -> list:
    """检查账号唯一性，返回重复列表"""
    seen = {}
    duplicates = []
    for acct in config.get("accounts", []):
        key = f"{acct['platform']}:{acct['username']}"
        if key in seen:
            duplicates.append(key)
        else:
            seen[key] = acct
    return duplicates


# ── 状态管理 ──────────────────────────────────────
def load_state(path: str) -> dict:
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"accounts": {}}


def save_state(state: dict, path: str):
    with open(path, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_last_fetch(state: dict, platform: str, username: str) -> datetime | None:
    key = f"{platform}:{username}"
    ts = state.get("accounts", {}).get(key, {}).get("last_fetch")
    if ts:
        return datetime.fromisoformat(ts)
    return None


def update_state(state: dict, platform: str, username: str,
                 last_tweet_id: str, fetched_at: datetime):
    key = f"{platform}:{username}"
    if "accounts" not in state:
        state["accounts"] = {}
    state["accounts"][key] = {
        "last_fetch": fetched_at.isoformat(),
        "last_id": last_tweet_id
    }


# ── 工具函数 ──────────────────────────────────────
def clean_text(text: str) -> str:
    """去除URL，压缩空白"""
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_new(state: dict, platform: str, username: str,
           created_at: datetime, tweet_id: str,
           catchup_days: int) -> bool:
    """判断内容是否应视为新内容（增量过滤）"""
    last = get_last_fetch(state, platform, username)
    if last is None:
        return True
    cutoff = datetime.now(timezone.utc) - timedelta(days=catchup_days)
    # tweets 的 created_at 是 UTC 但无时区信息，补上以便比较
    created_at_aware = created_at.replace(tzinfo=timezone.utc)
    if created_at_aware < cutoff:
        return False
    return created_at_aware > last


def is_worth_saving(tweet: dict, filters: dict) -> tuple[bool, str | None]:
    """
    过滤低价值内容。
    返回 (是否保存, 跳过原因)
    """
    text = tweet.get("text", "").strip()
    tweet_type = tweet.get("type", "tweet")
    text_clean = clean_text(text)

    # 关键词屏蔽
    blocked = filters.get("blocked_keywords", [])
    for kw in blocked:
        if kw.lower() in text_clean.lower():
            return False, f"屏蔽词「{kw}」"

    # 转推无原创评论
    if tweet_type == "retweet":
        if filters.get("skip_retweet_no_comment", True):
            if len(text_clean) < 30:
                return False, "转推无评论"

    # 仅链接/图片无文字
    if filters.get("skip_link_only", True):
        if len(text_clean) < 10:
            return False, "内容极少"

    # 字数门槛
    min_len = filters.get("min_text_length", 30)
    if len(text_clean) < min_len:
        return False, f"内容太短（{len(text_clean)}字）"

    return True, None


def apply_tags(text: str, tagging: dict) -> list[str]:
    """根据关键词匹配返回标签列表"""
    tags = ["claw-social-feed"]
    if not tagging.get("enabled", False):
        return tags

    text_lower = text.lower()
    keyword_map: dict[str, str] = tagging.get("keywords", {})

    for keywords, tag in keyword_map.items():
        for kw in keywords.split("/"):
            if kw.strip().lower() in text_lower:
                tags.append(tag.strip())
                break

    return list(set(tags))  # 去重


def save_to_obsidian(item: dict, tags: list, vault_base: str, platform: str, username: str):
    """将单条内容写入 Obsidian md 文件"""
    created = item["created_at"]
    if isinstance(created, str):
        dt = datetime.strptime(created, "%a %b %d %H:%M:%S +0000 %Y")
    else:
        dt = created

    date_str = dt.strftime("%Y-%m-%d")
    time_str = dt.strftime("%H%M%S")
    item_type = item.get("type", "unknown")
    item_id = item.get("id", "unknown")
    short_id = str(item_id)[-6:]

    folder = Path(vault_base) / f"@{username}"
    folder.mkdir(parents=True, exist_ok=True)

    filename = f"{date_str}_{time_str}_{short_id}.md"
    filepath = folder / filename

    # 跳过已存在的文件（幂等）
    if filepath.exists():
        return False, "已存在"

    # 预计算标签行（避免 f-string 内含反斜杠）
    tag_lines = "\n".join(f"  - {t}" for t in tags)

    frontmatter = f"""---
platform: {platform}
author: "@{username}"
type: {item_type}
date: {date_str}
time: "{created}"
url: {item.get("url", "")}
likes: {item.get("likes", 0)}
retweets: {item.get("retweets", 0)}
tags:
  - {platform}
  - "@{username}"
{tag_lines}
"""

    content = f"""## {date_str} {time_str[:2]}:{time_str[2:4]} · {item_type}

{item.get("text", "").strip()}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)

    return True, None


# ── bb-browser 调用 ────────────────────────────────
import shutil

def _find_bb_browser() -> str:
    """动态查找 bb-browser 路径"""
    # 先尝试 PATH 中直接找
    path = shutil.which("bb-browser")
    if path:
        return path
    # 尝试常见 node 全局 bin 路径
    import os
    home = os.path.expanduser("~")
    for node_ver in ["v20.19.5", "v22.0.0", "v21.0.0"]:
        candidate = os.path.join(home, f".nvm/versions/node/{node_ver}/bin/bb-browser")
        if os.path.isfile(candidate):
            return candidate
    # 兜底 PATH 追加常见 nvm bin 后重试
    for nvm_bin in [
        os.path.join(home, ".nvm/versions/node/v20.19.5/bin"),
        os.path.join(home, ".nvm/versions/node/v22.0.0/bin"),
        "/opt/homebrew/bin",
        "/usr/local/bin",
    ]:
        p = os.path.join(nvm_bin, "bb-browser")
        if os.path.isfile(p):
            return p
    return "bb-browser"  # 最后兜底，让 shell 找

BB_BROWSER_BIN = _find_bb_browser()


def fetch_account(platform: str, username: str, count: int) -> list[dict]:
    """通过 bb-browser --openclaw 获取用户内容"""
    import subprocess

    cmd = [
        BB_BROWSER_BIN,
        "site",
        f"{platform}/{get_adapter_cmd(platform)}",
        username,
        "--openclaw",
        "--json"
    ]

    env = os.environ.copy()
    bb_dir = str(Path(BB_BROWSER_BIN).parent)
    env["PATH"] = bb_dir + ":" + env.get("PATH", "")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            env=env
        )
        raw = result.stdout.strip()

        # 解析 bb-browser 的 JSON 信封
        idx = raw.find('{"id"')
        if idx < 0:
            idx = raw.find('{')
        end = raw.rfind('}') + 1
        data = json.loads(raw[idx:end])

        if data.get("success"):
            return data["data"].get("tweets", [])
        else:
            print(f"  [WARN] {platform}/{username}: {data.get('error', 'unknown error')}")
            return []

    except Exception as e:
        print(f"  [ERROR] {platform}/{username}: {e}")
        return []


def get_adapter_cmd(platform: str) -> str:
    """平台名 → bb-browser 子命令"""
    # 目前只支持这个映射，如有新平台需扩展
    return {
        "twitter": "tweets",
        "weibo": "user_posts",
        "reddit": "posts",
        "bilibili": "user_posts",
        "xiaohongshu": "user_posts",
        "hackernews": "top",
        "github": "repo",
        "v2ex": "hot",
        "zhihu": "hot",
        "xueqiu": "hot",
    }.get(platform, "hot")


# ── 主流程 ──────────────────────────────────────
def main():
    args = parse_args()
    verbose = args.verbose
    dry_run = args.dry_run

    config = load_config(args.config)
    state = load_state(str(DEFAULT_STATE))

    # 1. 账号唯一性检查
    dups = check_accounts(config)
    if dups:
        print(f"[WARN] 发现重复账号: {dups}，将只处理第一个")

    seen_keys = set()
    fetch_cfg = config.get("fetch", {})
    filters = config.get("filters", {})
    tagging = config.get("tagging", {})
    vault_base = os.path.expanduser(config.get("vault_base", "~/Documents/Obsidian Vault"))
    count = min(fetch_cfg.get("count", 20), 100)
    catchup_days = config.get("catchup_window_days", 3)

    total_saved = 0
    total_skipped = 0
    total_new = 0
    fetched_at = datetime.now(timezone.utc)

    accounts = config.get("accounts", [])
    if not accounts:
        print("[INFO] 配置文件中没有账号，请编辑 config.yaml 添加 accounts")
        return

    for acct in accounts:
        platform = acct["platform"]
        username = acct["username"]
        key = f"{platform}:{username}"

        if key in seen_keys:
            continue
        seen_keys.add(key)

        print(f"\n▶ {platform}/{username}")

        # 抓取
        items = fetch_account(platform, username, count)
        print(f"  抓取到 {len(items)} 条内容")

        last_new_id = None
        for item in items:
            item_id = item.get("id", "")

            # 解析时间
            try:
                created_str = item.get("created_at", "")
                if created_str:
                    dt = datetime.strptime(created_str, "%a %b %d %H:%M:%S +0000 %Y")
                else:
                    continue
            except Exception:
                continue

            # 增量判断
            if not is_new(state, platform, username, dt, item_id, catchup_days):
                continue
            total_new += 1

            # 过滤判断
            worth, reason = is_worth_saving(item, filters)
            if not worth:
                if verbose:
                    text_preview = clean_text(item.get("text", ""))[:40]
                    print(f"  ✗ {item_id}: {reason} | {text_preview}...")
                total_skipped += 1
                continue

            # 打标签
            tags = apply_tags(item.get("text", ""), tagging)

            # 存文件
            if not dry_run:
                saved, err = save_to_obsidian(item, tags, vault_base, platform, username)
                if err == "已存在":
                    if verbose:
                        print(f"  ⏭ {item_id}: 已存在，跳过")
                else:
                    text_preview = clean_text(item.get("text", ""))[:50]
                    print(f"  ✓ {item_id}: {text_preview}...")
                    print(f"    标签: {tags}")
                    total_saved += 1
            else:
                text_preview = clean_text(item.get("text", ""))[:50]
                print(f"  [DRY] {item_id}: {text_preview}...")

            last_new_id = item_id

        # 更新状态
        if last_new_id and not dry_run:
            update_state(state, platform, username, last_new_id, fetched_at)
            save_state(state, str(DEFAULT_STATE))
            print(f"  状态已更新（last_id: {last_new_id}）")

    print(f"\n{'='*50}")
    print(f"完成: 新内容 {total_new} 条 | 存入 {total_saved} | 过滤 {total_skipped}")


if __name__ == "__main__":
    main()
