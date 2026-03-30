#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pylint>=3.0",
#   "pyyaml>=6.0",
#   "pygithub>=2.1",
#   "requests>=2.31",
#   "click>=8.1",
#   "rich>=13.0",
# ]
# ///
"""
Convenience entry point — runnable directly via uv or python.

Usage with uv (no install required):
  uv run scripts/lint_pr.py pr 42
  uv run scripts/lint_pr.py staged --format text
  uv run scripts/lint_pr.py files src/ --format markdown
  uv run scripts/lint_pr.py diff changes.patch --config .linting-rules.yml

Usage after `uv sync`:
  uv run lint-pr pr 42
"""

import sys
from pathlib import Path

# Allow running from repo root without installation
sys.path.insert(0, str(Path(__file__).parent.parent))

from pylinter_assist.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
