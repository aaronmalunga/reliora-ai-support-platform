"""Typed contracts used by Reliora evaluators."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EvaluationFinding(BaseModel):
    """Result produced by one deterministic behavioural evaluator."""

    model_config = ConfigDict(frozen=True)

    invariant_id: str = Field(pattern=r"^INV-\d{3}$")
    passed: bool
    message: str
    evidence: dict[str, Any] = Field(default_factory=dict)