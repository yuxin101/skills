"""CLI entry point for pylinter-assist."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import click

from pylinter_assist.config import load_config
from pylinter_assist.linter import Linter
from pylinter_assist.reporter import render


@click.group()
def main():
    """pylinter-assist: context-aware Python linting with smart pattern heuristics."""


@main.command("pr")
@click.argument("pr_number", type=int)
@click.option("--repo", envvar="GITHUB_REPOSITORY", help="owner/repo (defaults to $GITHUB_REPOSITORY)")
@click.option("--token", envvar="GITHUB_TOKEN", help="GitHub token (defaults to $GITHUB_TOKEN)")
@click.option("--format", "fmt", default=None, type=click.Choice(["text", "json", "markdown"]), help="Output format")
@click.option("--config", "config_path", default=None, help="Path to .linting-rules.yml")
@click.option("--post-comment/--no-post-comment", default=None, help="Post result as PR comment")
@click.option("--fail-on-error/--no-fail-on-error", default=None)
@click.option("--fail-on-warning/--no-fail-on-warning", default=None)
def lint_pr(pr_number, repo, token, fmt, config_path, post_comment, fail_on_error, fail_on_warning):
    """Lint files changed in a GitHub pull request."""
    cfg = load_config(config_path)
    _apply_overrides(cfg, fmt, post_comment, fail_on_error, fail_on_warning)

    if not repo:
        click.echo("ERROR: --repo or $GITHUB_REPOSITORY required", err=True)
        sys.exit(2)

    diff = _fetch_pr_diff(repo, pr_number, token)
    linter = Linter(cfg)
    report = linter.lint_diff(diff, base_dir=".")

    output = render(report, fmt=cfg["output"]["format"], include_info=cfg["output"]["include_info"])
    click.echo(output)

    if cfg["github"].get("post_comment") and token and repo:
        _post_github_comment(repo, pr_number, token, output)

    _exit_with_code(report, cfg)


@main.command("staged")
@click.option("--format", "fmt", default=None, type=click.Choice(["text", "json", "markdown"]))
@click.option("--config", "config_path", default=None)
def lint_staged(fmt, config_path):
    """Lint git-staged files."""
    cfg = load_config(config_path)
    _apply_overrides(cfg, fmt)

    linter = Linter(cfg)
    report = linter.lint_staged(base_dir=".")

    output = render(report, fmt=cfg["output"]["format"], include_info=cfg["output"]["include_info"])
    click.echo(output)
    _exit_with_code(report, cfg)


@main.command("diff")
@click.argument("diff_file", type=click.Path(exists=True))
@click.option("--format", "fmt", default=None, type=click.Choice(["text", "json", "markdown"]))
@click.option("--config", "config_path", default=None)
def lint_diff(diff_file, fmt, config_path):
    """Lint files referenced in a unified diff file."""
    cfg = load_config(config_path)
    _apply_overrides(cfg, fmt)

    diff_text = Path(diff_file).read_text()
    linter = Linter(cfg)
    report = linter.lint_diff(diff_text, base_dir=".")

    output = render(report, fmt=cfg["output"]["format"], include_info=cfg["output"]["include_info"])
    click.echo(output)
    _exit_with_code(report, cfg)


@main.command("files")
@click.argument("paths", nargs=-1, required=True, type=click.Path())
@click.option("--format", "fmt", default=None, type=click.Choice(["text", "json", "markdown"]))
@click.option("--config", "config_path", default=None)
def lint_files(paths, fmt, config_path):
    """Lint specific files or directories."""
    cfg = load_config(config_path)
    _apply_overrides(cfg, fmt)

    all_files: list[str] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            all_files.extend(str(f) for f in path.rglob("*.py"))
        else:
            all_files.append(str(path))

    linter = Linter(cfg)
    report = linter.lint_files(all_files)

    output = render(report, fmt=cfg["output"]["format"], include_info=cfg["output"]["include_info"])
    click.echo(output)
    _exit_with_code(report, cfg)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _apply_overrides(cfg, fmt=None, post_comment=None, fail_on_error=None, fail_on_warning=None):
    if fmt:
        cfg["output"]["format"] = fmt
    if post_comment is not None:
        cfg["github"]["post_comment"] = post_comment
    if fail_on_error is not None:
        cfg["github"]["fail_on_error"] = fail_on_error
    if fail_on_warning is not None:
        cfg["github"]["fail_on_warning"] = fail_on_warning


def _fetch_pr_diff(repo: str, pr_number: int, token: str | None) -> str:
    import requests  # noqa: PLC0415

    headers = {"Accept": "application/vnd.github.v3.diff"}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text


def _post_github_comment(repo: str, pr_number: int, token: str, body: str):
    import requests  # noqa: PLC0415

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    payload = {"body": body}
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    if not resp.ok:
        click.echo(f"Warning: could not post comment: {resp.status_code} {resp.text}", err=True)


def _exit_with_code(report, cfg):
    fail_on_error = cfg["github"].get("fail_on_error", True)
    fail_on_warning = cfg["github"].get("fail_on_warning", False)

    if fail_on_error and report.has_errors():
        sys.exit(1)
    if fail_on_warning and report.has_warnings():
        sys.exit(1)
    sys.exit(0)
