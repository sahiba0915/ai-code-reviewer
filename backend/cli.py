from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from shutil import which
from typing import Optional

try:
    from reviewer import review_structured  # type: ignore
    from schema import Severity  # type: ignore
except ModuleNotFoundError:
    from backend.reviewer import review_structured  # type: ignore
    from backend.schema import Severity  # type: ignore


def _read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _resolve_gh_executable() -> str:
    gh = which("gh")
    if gh:
        return gh

    # Common Windows install locations (winget/msi)
    candidates = [
        r"C:\Program Files\GitHub CLI\gh.exe",
        r"C:\Program Files (x86)\GitHub CLI\gh.exe",
        str(Path.home() / "AppData" / "Local" / "Programs" / "GitHub CLI" / "gh.exe"),
    ]
    for p in candidates:
        if Path(p).exists():
            return p

    raise RuntimeError(
        "GitHub CLI 'gh' not found in PATH for this Python process. "
        "Open a new terminal after installing GitHub CLI, or pass the PR diff via --path."
    )


def _run_gh_pr_diff(pr_number: int, repo: Optional[str]) -> str:
    gh = _resolve_gh_executable()
    cmd = [gh]
    if repo:
        cmd += ["-R", repo]
    cmd += ["pr", "diff", str(pr_number), "--color=never"]
    try:
        completed = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return completed.stdout
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or "").strip()
        raise RuntimeError(f"Failed to fetch PR diff via gh. {stderr}".strip())


def _sev_icon_and_label(sev: Severity) -> tuple[str, str]:
    if sev == Severity.HIGH:
        return "▲", "HIGH"
    if sev == Severity.MEDIUM:
        return "▲", "MEDIUM"
    return "▲", "LOW"


def _print_report(*, title: str, result) -> None:
    print(title)
    print()

    if not result.issues:
        print("No issues found.")
        return

    # Stable ordering: HIGH -> MEDIUM -> LOW, then file/line
    rank = {Severity.HIGH: 0, Severity.MEDIUM: 1, Severity.LOW: 2}
    issues = sorted(
        result.issues,
        key=lambda i: (rank.get(i.severity, 9), i.file or "", int(i.line_number or 1)),
    )

    high = sum(1 for i in issues if i.severity == Severity.HIGH)
    medium = sum(1 for i in issues if i.severity == Severity.MEDIUM)
    low = sum(1 for i in issues if i.severity == Severity.LOW)

    for issue in issues:
        icon, label = _sev_icon_and_label(issue.severity)
        print(f"{icon} SEVERITY: {label} — {issue.file}:{issue.line_number}")
        print(issue.explanation)
        print(f"Suggested fix: {issue.suggested_fix}")
        print()

    print(f"{len(issues)} issues found · {high} high · {medium} medium · {low} low")
    print(f"Overall risk: {result.overall_risk.value}")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="codereview", description="Local AI code review (Ollama).")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--path", type=str, help="Path to a source file to review.")
    src.add_argument("--pr", type=int, help="GitHub Pull Request number to review (via gh pr diff).")
    parser.add_argument("--repo", type=str, default=None, help="Optional GitHub repo override: owner/name")
    parser.add_argument("--language", type=str, default=None, help="Optional language hint (e.g. python).")
    parser.add_argument("--model", type=str, default="llama3", help="Ollama model name (default: llama3).")
    args = parser.parse_args(argv)

    if args.path:
        path = Path(args.path).expanduser().resolve()
        code = _read_text_file(path)
        file_label = str(path).replace("\\", "/")
        title = f"codereview --path {file_label}"
        result = review_structured(code=code, language=args.language, file_label=file_label, model=args.model)
        _print_report(title=title, result=result)
        return 0

    diff = _run_gh_pr_diff(args.pr, args.repo)
    file_label = f"PR#{args.pr}"
    title = f"codereview --pr {args.pr}"
    result = review_structured(code=diff, language=args.language or "diff", file_label=file_label, model=args.model)
    _print_report(title=title, result=result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

