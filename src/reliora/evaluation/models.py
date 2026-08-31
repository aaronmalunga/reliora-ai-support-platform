"""Typed contracts used by Reliora evaluators."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EvaluationFinding(BaseModel):
    """Result produced by one deterministic Reliora evaluator."""

    model_config = ConfigDict(frozen=True)

    evaluation_id: str = Field(pattern=r"^(?:INV|FACT)-\d{3}$")
    passed: bool
    message: str
    evidence: dict[str, Any] = Field(default_factory=dict)