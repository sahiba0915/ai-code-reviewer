def build_review_prompt(code: str, language: str | None = None) -> str:
    """
    Build a detailed prompt instructing the LLM to perform a thorough code review.

    Keeping this logic in a dedicated module makes it easy to iterate on the
    review instructions without touching the API or LLM client code.
    """
    language_note = ""
    if language and language.lower() not in ("auto", ""):
        language_note = f" The code is {language}. Apply {language} conventions and best practices where relevant.\n\n"

    template = """You are a senior software engineer performing a concise, actionable code review.
{language_note}Analyze the code below and respond with clear sections. For each finding, state the issue and a concrete fix when possible. Use this structure:

## Bugs & correctness
- List potential bugs, logic errors, or edge cases (e.g. null/zero, empty input). Say how to fix each.

## Security & robustness
- Input validation, injection risks, error handling, or unsafe assumptions.

## Performance
- Inefficient patterns, unnecessary work, or better algorithms. Be specific.

## Style & best practices
- Naming, readability, DRY violations, or language/framework best practices.

## Refactoring suggestions
- Short, actionable improvements (extract function, simplify condition, etc.).

Keep each bullet brief (1–2 sentences). If a section has nothing to report, write "None." Do not repeat the code; only comment on it.

Code to review:

```
{code}
```
"""
    return template.format(language_note=language_note, code=code)


def build_structured_review_prompt(
    *,
    code: str,
    language: str | None = None,
    file_label: str = "unknown",
    start_line: int = 1,
    schema_json: str,
) -> str:
    language_note = ""
    if language and language.lower() not in ("auto", ""):
        language_note = (
            f" The code is {language}. Apply {language} conventions and best practices where relevant.\n\n"
        )

    # IMPORTANT: Ollama's /api/generate does not guarantee JSON mode, so we
    # must be extremely explicit and keep the output surface area small.
    return f"""You are a senior software engineer performing a code review.
{language_note}Return ONLY valid JSON that matches this schema exactly (no markdown, no prose):
{schema_json}

Rules:
- Output must be a single JSON object.
- Use severity as one of: HIGH, MEDIUM, LOW (uppercase).
- Prefer categories like: security, correctness, reliability, performance, style, testing, maintainability.
- Use the provided file label in the "file" field when relevant: {file_label}
- Use 1-based line numbers relative to the ORIGINAL file; the snippet starts at line {start_line}.
- Be specific and actionable in "suggested_fix".
- If there are no issues, return an empty "issues" list and a short summary.

Code snippet:
```text
{code}
```
"""

