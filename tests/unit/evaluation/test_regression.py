"""Unit tests for deterministic evaluator regression dispatch."""

import pytest

from reliora.evaluation.regression import evaluate_regression_case


def test_inv_004_case_dispatches_to_bug_workflow_evaluator() -> None:
    case = {
        "evaluation_id": "INV-004",
        "inputs": {
            "missing_fields": [
                "steps_to_reproduce",
                "environment",
            ],
            "requested_fields": [
                "steps_to_reproduce",
            ],
        },
    }

    result = evaluate_regression_case(case)

    assert result.evaluation_id == "INV-004"
    assert result.passed is True


def test_inv_012_case_dispatches_to_leakage_evaluator() -> None:
    case = {
        "evaluation_id": "INV-012",
        "inputs": {
            "response": "HUMAN HANDOFF: Please contact support.",
        },
    }

    result = evaluate_regression_case(case)

    assert result.evaluation_id == "INV-012"
    assert result.passed is False


def test_fact_001_case_dispatches_to_factual_evaluator() -> None:
    case = {
        "evaluation_id": "FACT-001",
        "inputs": {
            "response": (
                "Returns are accepted within 30 days when items are unused."
            ),
            "required_facts": {
                "return_window": [
                    "30 days",
                ],
                "unused_condition": [
                    "unused",
                ],
            },
        },
    }

    result = evaluate_regression_case(case)

    assert result.evaluation_id == "FACT-001"
    assert result.passed is True


def test_unknown_evaluation_id_is_rejected() -> None:
    case = {
        "evaluation_id": "INV-999",
        "inputs": {},
    }

    with pytest.raises(
        ValueError,
        match="Unsupported evaluation_id: INV-999",
    ):
        evaluate_regression_case(case)