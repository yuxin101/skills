#!/usr/bin/env python3
"""novel-writing CLI: 小说创作辅助工具"""
import sys
import os
import json
import re
import argparse
from pathlib import Path
from datetime import datetime

NOVEL_DIR = Path("novel")

def safe_name(name):
    """校验项目名，防止路径穿越"""
    import re
    if not re.match(r'^[\w-]+$', name):
        return None
    if '..' in name:
        return None
    return name

def cmd_init(name):
    """初始化新书项目"""
    novel = NOVEL_DIR / name
    if novel.exists():
        print(f"项目 {name} 已存在")
        return
    novel.mkdir(parents=True, exist_ok=True)
    (novel / "settings").mkdir(exist_ok=True)
    (novel / "chapters").mkdir(exist_ok=True)
    (novel / "tracker").mkdir(exist_ok=True)
    state = {"name": name, "current_arc": 1, "current_chapter": 1, "word_count_today": 0, "last_updated": ""}
    with open(novel / "state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    (novel / "settings" / "world.md").write_text("# 世界观设定\n\n", encoding="utf-8")
    (novel / "chapters" / "outline.md").write_text("# 大纲\n\n", encoding="utf-8")
    (novel / "tracker" / "foreshadowing.md").write_text("# 伏笔追踪\n\n", encoding="utf-8")
    (novel / "tracker" / "conflicts.md").write_text("# 冲突记录\n\n", encoding="utf-8")
    (novel / "tracker" / "feedback.md").write_text("# 读者反馈\n\n", encoding="utf-8")
    print(f"✅ 项目 {name} 创建成功")

def cmd_write(novel_name, chapter, content):
    """撰写章节"""
    if not safe_name(novel_name):
        print("❌ 项目名只能包含字母、数字、下划线、中划线")
        return
    novel = NOVEL_DIR / novel_name
    if not novel.exists():
        print(f"项目 {novel_name} 不存在，请先运行 novel init")
        return
    arc = (chapter - 1) // 30 + 1
    arc_dir = novel / "chapters" / f"arc-{arc}"
    arc_dir.mkdir(exist_ok=True)
    chapter_file = arc_dir / f"chapter-{chapter:03d}.txt"
    chapter_file.write_text(content, encoding="utf-8")
    state_file = novel / "state.json"
    state = json.loads(state_file.read_text(encoding="utf-8"))
    state["current_chapter"] = chapter
    state["word_count_today"] += len(content)
    state["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 第{chapter}章已保存，字数：{len(content)}")

def cmd_check(novel_name, chapter):
    """伏笔检测"""
    if not safe_name(novel_name):
        print("❌ 项目名只能包含字母、数字、下划线、中划线")
        return
    novel = NOVEL_DIR / novel_name
    fs_file = novel / "tracker" / "foreshadowing.md"
    if not fs_file.exists():
        print("无伏笔记录")
        return
    content = fs_file.read_text(encoding="utf-8")
    # 找本章相关伏笔
    pending = []
    for line in content.split("\n"):
        if f"章{chapter}" in line and "→" in line:
            pending.append(line.strip())
    if pending:
        print(f"⚠️ 第{chapter}章有 {len(pending)} 条伏笔待回收：")
        for p in pending: print(f"  {p}")
    else:
        print(f"✅ 第{chapter}章无待回收伏笔")

def cmd_feedback(novel_name, chapter, feedback):
    """读者反馈入库"""
    if not safe_name(novel_name):
        print("❌ 项目名只能包含字母、数字、下划线、中划线")
        return
    novel = NOVEL_DIR / novel_name
    fb_file = novel / "tracker" / "feedback.md"
    entry = f"- [章{chapter}] {feedback} ({datetime.now().strftime('%Y-%m-%d')})\n"
    with open(fb_file, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"✅ 反馈已入库（第{chapter}章）")

def cmd_conflict(novel_name, new_content):
    """冲突检测"""
    if not safe_name(novel_name):
        print("❌ 项目名只能包含字母、数字、下划线、中划线")
        return
    novel = NOVEL_DIR / novel_name
    if not novel.exists():
        print("项目不存在")
        return
    conflicts = []
    for md in (novel / "settings").rglob("*.md"):
        setting = md.read_text(encoding="utf-8")
        for word in new_content.split()[:20]:
            if len(word) >= 3 and word in setting:
                conflicts.append(f"⚠️ '{word}' 与 {md.relative_to(novel)} 设定冲突")
    if conflicts:
        for c in conflicts: print(c)
    else:
        print("✅ 未检测到明显冲突")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="小说创作辅助CLI")
    parser.add_argument("command", choices=["init", "write", "check", "feedback", "conflict"])
    parser.add_argument("--novel", default="main")
    parser.add_argument("--chapter", type=int, default=1)
    parser.add_argument("--content", default="")
    parser.add_argument("--feedback", default="")
    args = parser.parse_args(sys.argv[2:]) if len(sys.argv) > 2 else argparse.Namespace()
    
    if args.command == "init":
        cmd_init(sys.argv[2] if len(sys.argv) > 2 else "main")
    elif args.command == "write":
        cmd_write(args.novel, args.chapter, args.content)
    elif args.command == "check":
        cmd_check(args.novel, args.chapter)
    elif args.command == "feedback":
        cmd_feedback(args.novel, args.chapter, args.feedback)
    elif args.command == "conflict":
        cmd_conflict(args.novel, args.content)
