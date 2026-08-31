"""Execution of frozen Stage-1 reproduction cases."""

from typing import Any

from reliora.evaluation.bug_workflow import (
    BugField,
    evaluate_incremental_bug_collection,
)
from reliora.evaluation.factual import evaluate_required_fact_completeness
from reliora.evaluation.leakage import evaluate_internal_information_leakage


def evaluate_reproduction_case(case: dict[str, Any]) -> dict[str, Any]:
    """Execute one versioned reproduction case against its evaluator."""

    if not case["executable"]:
        return {
            "case_id": case["case_id"],
            "evaluation_id": case["evaluation_id"],
            "status": "DOCUMENTED",
            "executed": False,
            "expectation_met": None,
            "evaluator_passed": None,
            "message": case["reason_not_executable"],
        }

    evaluation_id = case["evaluation_id"]

    if evaluation_id == "INV-004":
        annotation = case["reviewed_annotation"]

        missing_fields = [
            BugField(field)
            for field in annotation["missing_fields"]
        ]
        requested_fields = [
            BugField(field)
            for field in annotation["requested_fields"]
        ]

        finding = evaluate_incremental_bug_collection(
            missing_fields=missing_fields,
            requested_fields=requested_fields,
        )

    elif evaluation_id == "INV-012":
        finding = evaluate_internal_information_leakage(case["response"])

    elif evaluation_id == "FACT-001":
        required_facts = {
            assertion["fact_id"]: assertion["accepted_patterns"]
            for assertion in case["reviewed_assertions"]
            if assertion["required"]
        }

        finding = evaluate_required_fact_completeness(
            response=case["response"],
            required_facts=required_facts,
        )

    else:
        raise ValueError(
            f"Unsupported evaluation_id: {evaluation_id}"
        )

    expected_passed = case["expected_evaluator_passed"]
    expectation_met = finding.passed == expected_passed

    if expectation_met and finding.passed is False:
        status = "DETECTED"
    elif expectation_met:
        status = "CONFIRMED"
    else:
        status = "MISMATCH"

    return {
        "case_id": case["case_id"],
        "evaluation_id": finding.evaluation_id,
        "status": status,
        "executed": True,
        "expectation_met": expectation_met,
        "expected_evaluator_passed": expected_passed,
        "evaluator_passed": finding.passed,
        "message": finding.message,
        "evidence": finding.evidence,
    }