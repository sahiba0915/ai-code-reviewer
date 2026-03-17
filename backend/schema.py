from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class Severity(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

    @classmethod
    def from_any(cls, value: object) -> "Severity":
        if value is None:
            return cls.LOW
        s = str(value).strip().upper()
        if s in ("HIGH", "H"):
            return cls.HIGH
        if s in ("MEDIUM", "MID", "M"):
            return cls.MEDIUM
        if s in ("LOW", "L"):
            return cls.LOW
        return cls.LOW


class ReviewIssue(BaseModel):
    file: str = Field(default="unknown")
    line_number: int = Field(default=1, ge=1)
    severity: Severity = Field(default=Severity.LOW)
    category: str = Field(default="general")
    explanation: str = Field(min_length=1)
    suggested_fix: str = Field(min_length=1)

    @validator("file", pre=True, always=True)
    def _normalize_file(cls, v: object) -> str:
        s = (str(v).strip() if v is not None else "") or "unknown"
        return s

    @validator("severity", pre=True, always=True)
    def _normalize_severity(cls, v: object) -> Severity:
        return Severity.from_any(v)

    @validator("category", pre=True, always=True)
    def _normalize_category(cls, v: object) -> str:
        s = (str(v).strip() if v is not None else "") or "general"
        return s


class CodeReviewResult(BaseModel):
    issues: List[ReviewIssue] = Field(default_factory=list)
    summary: str = Field(default="")
    overall_risk: Severity = Field(default=Severity.LOW)

    model: Optional[str] = None
    analyzed_units: Optional[int] = None

    @validator("overall_risk", pre=True, always=True)
    def _normalize_overall_risk(cls, v: object) -> Severity:
        return Severity.from_any(v)

