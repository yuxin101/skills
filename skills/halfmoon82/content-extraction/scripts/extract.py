#!/usr/bin/env python3
"""OpenClaw content-extraction executor scaffold.

This executable turns a URL into a concrete extraction workflow.
It does not talk to external OpenClaw tools directly; instead it emits the
steps, target tool, and output contract so the next automation layer can run it.

Usage:
    python3 extract.py 'https://mp.weixin.qq.com/s/xxx'
    python3 extract.py --json 'https://www.feishu.cn/docx/xxx'
    python3 extract.py --title 'Demo Title' 'https://example.com'
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

from extract_router import RoutePlan, classify_url


@dataclass
class ExtractionSpec:
    plan: RoutePlan
    save_path: str
    summary_contract: List[str]
    output_contract: List[str]
    execution_layers: List[str]


def default_save_path(plan: RoutePlan, title: str | None = None) -> str:
    name = plan.save_name if plan.save_name else (title or plan.source_type)
    safe = name.replace("/", "_")
    return str(Path("extracted") / f"{safe}.md")


def build_spec(url: str, title: str | None = None) -> ExtractionSpec:
    plan = classify_url(url, title)
    save_path = default_save_path(plan, title)

    if plan.handler == "browser":
        exec_layers = [
            "browser: open URL",
            "browser: wait for render",
            "browser: extract title/author/date/body/images",
            "markdown: write frontmatter +正文",
        ]
    elif plan.handler == "feishu":
        exec_layers = [
            "feishu: resolve doc/wiki token",
            "feishu: read structured blocks",
            "markdown: map blocks to headings/lists/code/todo/table",
            "markdown: write metadata +正文",
        ]
    elif plan.handler == "transcript":
        exec_layers = [
            "transcript: fetch captions / transcript",
            "markdown: normalize transcript",
            "markdown: write metadata +正文",
        ]
    else:
        exec_layers = [
            "web: try r.jina.ai",
            "web: fallback to defuddle.md",
            "web: fallback to web_fetch",
            "browser: last fallback",
            "markdown: write metadata +正文",
        ]

    return ExtractionSpec(
        plan=plan,
        save_path=save_path,
        summary_contract=[
            "title",
            "source",
            "url",
            "short summary",
            "save path",
        ],
        output_contract=[
            "markdown",
            "frontmatter when useful",
            "clean body text",
            "keep images/tables/code blocks when possible",
        ],
        execution_layers=exec_layers,
    )


def spec_to_markdown(spec: ExtractionSpec) -> str:
    p = spec.plan
    lines = [
        f"**URL**: {p.input_url}",
        f"**来源**: {p.source_type}",
        f"**处理器**: {p.handler}",
        f"**保存路径**: {spec.save_path}",
        "",
        "### Execution Layers",
    ]
    lines.extend([f"- {x}" for x in spec.execution_layers])
    lines.append("")
    lines.append("### Summary Contract")
    lines.extend([f"- {x}" for x in spec.summary_contract])
    lines.append("")
    lines.append("### Output Contract")
    lines.extend([f"- {x}" for x in spec.output_contract])
    lines.append("")
    lines.append("### Fallback Chain")
    lines.extend([f"- {x}" for x in p.fallback_chain])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenClaw content-extraction executor scaffold")
    parser.add_argument("url")
    parser.add_argument("--title", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    spec = build_spec(args.url, args.title)
    if args.json:
        out = asdict(spec)
        out["plan"] = asdict(spec.plan)
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(spec_to_markdown(spec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
