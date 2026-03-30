#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "VERSION.txt",
    "config.template.json",
    "examples.md",
    "README.zh-CN.md",
    "README.en.md",
    "RELEASE.md",
    "assets/logo.svg",
    "assets/cover.svg",
    "assets/flow.svg",
    "subskills/search/SKILL.md",
    "subskills/generate-image/SKILL.md",
    "subskills/generate-video/SKILL.md",
    "subskills/generate-3d/SKILL.md",
    "subskills/logo-design/SKILL.md",
    "subskills/product-image/SKILL.md",
    "subskills/upload/SKILL.md",
    "subskills/report/SKILL.md",
    "playbooks/design-intake.md",
    "scripts/check_tools_mapping.py",
    "scripts/build_release_zip.py",
]


def load_version(skill_root: Path) -> str:
    version_path = skill_root / "VERSION.txt"
    return version_path.read_text(encoding="utf-8").strip()


def load_config(skill_root: Path) -> dict:
    config_path = skill_root / "config.template.json"
    return json.loads(config_path.read_text(encoding="utf-8"))


def check_required_files(skill_root: Path) -> list[str]:
    missing = []
    for rel in REQUIRED_FILES:
        if not (skill_root / rel).exists():
            missing.append(rel)
    return missing


def check_plaintext_key(skill_root: Path, config: dict) -> list[str]:
    issues = []
    gateway = config.get("gateway", {})
    key_value = gateway.get("key_value", "")
    if isinstance(key_value, str) and key_value.strip():
        issues.append("config.template.json: gateway.key_value 必须为空字符串")

    key_pattern = re.compile(r"\b[a-fA-F0-9]{32}\b")
    for p in skill_root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in {"dist", "__pycache__", ".git"} for part in p.parts):
            continue
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".zip", ".ico"}:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if key_pattern.search(text):
            issues.append(f"{p.relative_to(skill_root)}: 检测到疑似明文密钥")
    return issues


def main() -> int:
    skill_root = Path(__file__).resolve().parent.parent
    missing = check_required_files(skill_root)
    if missing:
        print("缺失文件：")
        for m in missing:
            print(f"- {m}")
        return 1

    version = load_version(skill_root)
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        print("VERSION.txt: 必须为 x.y.z 语义化版本格式")
        return 1

    config = load_config(skill_root)
    if config.get("pipeline", {}).get("forbid_plaintext_key") is not True:
        print("config.template.json: pipeline.forbid_plaintext_key 必须为 true")
        return 1

    issues = check_plaintext_key(skill_root, config)
    if issues:
        print("安全校验失败：")
        for i in issues:
            print(f"- {i}")
        return 1

    print("validate_release: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
