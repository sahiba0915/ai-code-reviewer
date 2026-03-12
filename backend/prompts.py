def build_review_prompt(code: str) -> str:
    """
    Build a detailed prompt instructing the LLM to perform a thorough code review.

    Keeping this logic in a dedicated module makes it easy to iterate on the
    review instructions without touching the API or LLM client code.
    """

    template = """You are a senior software engineer performing a code review.

Analyze the following code and provide:
- Bugs
- Performance issues
- Best practices
- Refactoring suggestions

Code:
{code}
"""
    return template.format(code=code)

