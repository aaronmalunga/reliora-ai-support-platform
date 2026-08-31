"""Execution of designed deterministic evaluator regression cases."""

from typing import Any

from reliora.evaluation.bug_workflow import (
    BugField,
    evaluate_incremental_bug_collection,
)
from reliora.evaluation.factual import evaluate_required_fact_completeness
from reliora.evaluation.leakage import evaluate_internal_information_leakage
from reliora.evaluation.models import EvaluationFinding


def evaluate_regression_case(case: dict[str, Any]) -> EvaluationFinding:
    """Dispatch one designed regression fixture to its evaluator."""

    evaluation_id = case["evaluation_id"]
    inputs = case["inputs"]

    if evaluation_id == "INV-004":
        missing_fields = [
            BugField(field)
            for field in inputs["missing_fields"]
        ]
        requested_fields = [
            BugField(field)
            for field in inputs["requested_fields"]
        ]

        return evaluate_incremental_bug_collection(
            missing_fields=missing_fields,
            requested_fields=requested_fields,
        )

    if evaluation_id == "INV-012":
        return evaluate_internal_information_leakage(
            inputs["response"],
        )

    if evaluation_id == "FACT-001":
        return evaluate_required_fact_completeness(
            response=inputs["response"],
            required_facts=inputs["required_facts"],
        )

    raise ValueError(
        f"Unsupported evaluation_id: {evaluation_id}"
    )