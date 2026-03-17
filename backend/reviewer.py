from __future__ import annotations

import json
from typing import Iterable, List, Optional, Tuple

import requests

try:
    # When running from inside the backend directory (e.g. `uvicorn main:app`)
    from prompts import build_structured_review_prompt  # type: ignore
    from schema import CodeReviewResult, ReviewIssue, Severity  # type: ignore
except ModuleNotFoundError:
    # When running from the repo root (e.g. `python backend/cli.py`)
    from backend.prompts import build_structured_review_prompt  # type: ignore
    from backend.schema import CodeReviewResult, ReviewIssue, Severity  # type: ignore


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def _call_ollama_generate(*, prompt: str, model: str = MODEL_NAME, timeout_s: int = 180) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=timeout_s)
    response.raise_for_status()
    data = response.json()
    return (data.get("response", "") or "").strip()


def review_code(prompt: str) -> str:
    """
    Backwards-compatible: returns free-form text.
    """
    return _call_ollama_generate(prompt=prompt)


def _chunk_lines(text: str, *, max_lines: int) -> Iterable[Tuple[int, str]]:
    lines = text.splitlines()
    if not lines:
        yield 1, ""
        return
    for i in range(0, len(lines), max_lines):
        start_line = i + 1
        chunk = "\n".join(lines[i : i + max_lines])
        yield start_line, chunk


def _extract_json_object(text: str) -> Optional[str]:
    """
    Best-effort extraction of a single JSON object from model output.
    """
    s = text.strip()
    if not s:
        return None
    if s.startswith("{") and s.endswith("}"):
        return s
    first = s.find("{")
    last = s.rfind("}")
    if first == -1 or last == -1 or last <= first:
        return None
    candidate = s[first : last + 1].strip()
    if candidate.startswith("{") and candidate.endswith("}"):
        return candidate
    return None


def _severity_rank(sev: Severity) -> int:
    return {Severity.LOW: 1, Severity.MEDIUM: 2, Severity.HIGH: 3}.get(sev, 1)


def _compute_overall_risk(issues: List[ReviewIssue]) -> Severity:
    if not issues:
        return Severity.LOW
    worst = max((_severity_rank(i.severity) for i in issues), default=1)
    return {1: Severity.LOW, 2: Severity.MEDIUM, 3: Severity.HIGH}.get(worst, Severity.LOW)


def review_structured(
    *,
    code: str,
    language: str | None = None,
    file_label: str = "unknown",
    model: str = MODEL_NAME,
    max_chunk_lines: int = 220,
) -> CodeReviewResult:
    """
    Returns schema-enforced structured output (issues with severity, file, line).
    Uses chunking to handle large inputs and merges results.
    """
    schema_json = CodeReviewResult.schema_json(indent=2)

    merged_issues: List[ReviewIssue] = []
    analyzed_units = 0

    for start_line, chunk in _chunk_lines(code, max_lines=max_chunk_lines):
        prompt = build_structured_review_prompt(
            code=chunk,
            language=language,
            file_label=file_label,
            start_line=start_line,
            schema_json=schema_json,
        )
        raw = _call_ollama_generate(prompt=prompt, model=model)
        extracted = _extract_json_object(raw)

        if not extracted:
            merged_issues.append(
                ReviewIssue(
                    file=file_label,
                    line_number=start_line,
                    severity=Severity.MEDIUM,
                    category="reliability",
                    explanation="Model did not return valid JSON for this chunk.",
                    suggested_fix="Retry the review or reduce chunk size; ensure the model output is JSON-only.",
                )
            )
            analyzed_units += 1
            continue

        try:
            data = json.loads(extracted)
            result = CodeReviewResult.parse_obj(data)
        except Exception:
            merged_issues.append(
                ReviewIssue(
                    file=file_label,
                    line_number=start_line,
                    severity=Severity.MEDIUM,
                    category="reliability",
                    explanation="Failed to parse model JSON output into the expected schema.",
                    suggested_fix="Retry the review; if it persists, switch model or tighten the prompt.",
                )
            )
            analyzed_units += 1
            continue

        for issue in result.issues:
            # Line numbers are supposed to be absolute; but if the model returns
            # chunk-relative values, this nudges them into the right ballpark.
            if issue.line_number < start_line:
                issue.line_number = start_line + max(issue.line_number - 1, 0)
            if not issue.file or issue.file == "unknown":
                issue.file = file_label
            merged_issues.append(issue)

        analyzed_units += 1

    overall_risk = _compute_overall_risk(merged_issues)
    summary = (
        f"{len(merged_issues)} issue(s) found — overall risk: {overall_risk.value}"
        if merged_issues
        else "No issues found."
    )

    return CodeReviewResult(
        issues=merged_issues,
        summary=summary,
        overall_risk=overall_risk,
        model=model,
        analyzed_units=analyzed_units,
    )

