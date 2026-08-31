"""Deterministic factual-completeness evaluation."""

from collections.abc import Sequence

from reliora.evaluation.models import EvaluationFinding


def evaluate_required_fact_completeness(
    *,
    response: str,
    required_facts: dict[str, Sequence[str]],
) -> EvaluationFinding:
    """Check whether every required fact is represented in the response.

    Each fact may define multiple accepted textual patterns. A fact is
    considered present when at least one of its accepted patterns appears
    in the response, using case-insensitive matching.
    """

    normalized_response = response.casefold()

    missing_facts: list[str] = []
    matched_facts: list[str] = []

    for fact_id, accepted_patterns in required_facts.items():
        patterns = [pattern.casefold() for pattern in accepted_patterns]

        if any(pattern in normalized_response for pattern in patterns):
            matched_facts.append(fact_id)
        else:
            missing_facts.append(fact_id)

    passed = not missing_facts

    if passed:
        message = "All required facts are represented in the response."
    else:
        message = "One or more required facts are missing from the response."

    return EvaluationFinding(
        evaluation_id="FACT-001",
        passed=passed,
        message=message,
        evidence={
            "matched_facts": matched_facts,
            "missing_facts": missing_facts,
        },
    )