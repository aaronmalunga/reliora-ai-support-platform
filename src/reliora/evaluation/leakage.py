"""Deterministic checks for prohibited customer-visible information."""

import re

from reliora.evaluation.models import EvaluationFinding

_PROHIBITED_PATTERNS: dict[str, re.Pattern[str]] = {
    "human_handoff_route": re.compile(r"\bHUMAN HANDOFF\b"),
    "thinking_tag": re.compile(r"</?thinking\b[^>]*>", re.IGNORECASE),
}


def evaluate_internal_information_leakage(
    response: str,
) -> EvaluationFinding:
    """Evaluate INV-012 against customer-visible response text."""

    matches: dict[str, list[str]] = {}

    for name, pattern in _PROHIBITED_PATTERNS.items():
        found = pattern.findall(response)
        if found:
            matches[name] = found

    passed = not matches

    return EvaluationFinding(
        evaluation_id="INV-012",
        passed=passed,
        message=(
            "No prohibited internal markers detected."
            if passed
            else "Customer-visible response contains prohibited internal markers."
        ),
        evidence={"matches": matches},
    )