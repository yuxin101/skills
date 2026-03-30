#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qryma Search for ClawHub
A single-file search skill with multiple output formats
"""
import json
import os
import pathlib
import re
import sys
import urllib.request
from typing import Optional

QRYMA_DEFAULT_ENDPOINT = "https://search.qryma.com/api/web"


def load_key() -> Optional[str]:
    """Load Qryma API key from environment or config"""
    key = os.environ.get("QRYMA_API_KEY")
    if key:
        return key.strip()

    env_path = pathlib.Path.home() / ".qryma" / ".env"
    if not env_path.exists():
        env_path = pathlib.Path(".env")
    if env_path.exists():
        try:
            txt = env_path.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^\s*QRYMA_API_KEY\s*=\s*(.+?)\s*$", txt, re.M)
            if m:
                v = m.group(1).strip().strip('"').strip("'")
                if v:
                    return v
        except (OSError, IOError):
            pass

    return None


def load_endpoint() -> str:
    """Load Qryma API endpoint"""
    endpoint = os.environ.get("QRYMA_ENDPOINT")
    if endpoint:
        return endpoint.strip()

    env_path = pathlib.Path.home() / ".qryma" / ".env"
    if not env_path.exists():
        env_path = pathlib.Path(".env")
    if env_path.exists():
        try:
            txt = env_path.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^\s*QRYMA_ENDPOINT\s*=\s*(.+?)\s*$", txt, re.M)
            if m:
                v = m.group(1).strip().strip('"').strip("'")
                if v:
                    return v
        except (OSError, IOError):
            pass

    return QRYMA_DEFAULT_ENDPOINT


def search(
    query: str,
    max_results: int = 5,
    lang: str = "en",
    start: int = 0,
    safe: bool = False,
    detail: bool = False,
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> dict:
    """Execute search against Qryma API"""
    api_key = api_key or load_key()
    endpoint = endpoint or load_endpoint()

    if not api_key:
        raise SystemExit(
            "Missing QRYMA_API_KEY. Set env var QRYMA_API_KEY or add it to ~/.qryma/.env"
        )

    payload = {
        "query": query,
        "lang": lang,
        "start": start,
        "safe": safe,
        "detail": detail,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "ClawHub-Qryma-Search/1.0",
            "X-Api-Key": api_key,
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8", errors="replace")

    try:
        obj = json.loads(body)
    except json.JSONDecodeError:
        raise SystemExit(f"Qryma returned non-JSON: {body[:300]}")

    out = {
        "query": query,
        "results": [],
    }

    for r in (obj.get("organic") or [])[:max_results]:
        out["results"].append({
            "title": r.get("title"),
            "url": r.get("link"),
            "content": r.get("snippet"),
        })

    return out


def to_brave_like(obj: dict) -> dict:
    """Format result like Brave search (title/url/snippet)"""
    results = []
    for r in obj.get("results", []) or []:
        results.append({
            "title": r.get("title"),
            "url": r.get("url"),
            "snippet": r.get("content"),
        })
    out = {"query": obj.get("query"), "results": results}
    return out


def to_markdown(obj: dict) -> str:
    """Format result as human-readable Markdown"""
    lines = []
    for i, r in enumerate(obj.get("results", []) or [], 1):
        title = (r.get("title") or "").strip() or r.get("url") or "(no title)"
        url = r.get("url") or ""
        snippet = (r.get("content") or "").strip()
        lines.append(f"{i}. {title}")
        if url:
            lines.append(f"   {url}")
        if snippet:
            lines.append(f"   - {snippet}")
    return "\n".join(lines).strip() + "\n"


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Qryma Web Search")
    ap.add_argument("--api-key", help="Qryma API key")
    ap.add_argument("--query", required=True, help="Search query")
    ap.add_argument("--max-results", type=int, default=5, help="Max results (default: 5)")
    ap.add_argument("--lang", default="en", help="Language code (default: en) - [See available languages](https://developers.google.com/custom-search/docs/xml_results_appendices#interfaceLanguages)")
    ap.add_argument("--start", type=int, default=0, help="Start offset (default: 0)")
    ap.add_argument("--safe", action="store_true", help="Enable safe search (default: False)")
    ap.add_argument("--detail", action="store_true", help="Enable detailed results (default: False)")
    ap.add_argument(
        "--format",
        choices=["raw", "brave", "md"],
        default="md",
        help="Output format: raw | brave (title/url/snippet) | md (human-readable, default)"
    )

    args = ap.parse_args()

    res = search(
        query=args.query,
        max_results=max(1, min(args.max_results, 10)),
        lang=args.lang,
        start=args.start,
        safe=args.safe,
        detail=args.detail,
        api_key=args.api_key,
    )

    if args.format == "md":
        output = to_markdown(res)
        sys.stdout.buffer.write(output.encode('utf-8'))
        return

    if args.format == "brave":
        res = to_brave_like(res)

    json_str = json.dumps(res, ensure_ascii=False, default=str)
    sys.stdout.buffer.write(json_str.encode('utf-8'))
    sys.stdout.buffer.write(b'\n')


if __name__ == "__main__":
    main()
