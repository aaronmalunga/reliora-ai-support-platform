"""Unit tests for Stage-1 reproduction execution."""

from reliora.evaluation.reproduction import evaluate_reproduction_case


def test_inv_004_known_defect_is_detected() -> None:
    case = {
        "case_id": "REPRO-001",
        "evaluation_id": "INV-004",
        "executable": True,
        "expected_evaluator_passed": False,
        "reviewed_annotation": {
            "missing_fields": [
                "description",
                "steps_to_reproduce",
                "environment",
            ],
            "requested_fields": [
                "description",
                "steps_to_reproduce",
                "environment",
            ],
        },
    }

    result = evaluate_reproduction_case(case)

    assert result["status"] == "DETECTED"
    assert result["expectation_met"] is True
    assert result["evaluator_passed"] is False


def test_inv_012_known_route_leak_is_detected() -> None:
    case = {
        "case_id": "REPRO-002",
        "evaluation_id": "INV-012",
        "executable": True,
        "expected_evaluator_passed": False,
        "response": (
            "HUMAN HANDOFF\n\n"
            "For further assistance, please contact support."
        ),
    }

    result = evaluate_reproduction_case(case)

    assert result["status"] == "DETECTED"
    assert result["expectation_met"] is True
    assert result["evaluator_passed"] is False


def test_non_executable_observation_is_documented() -> None:
    case = {
        "case_id": "REPRO-003",
        "evaluation_id": "INV-012",
        "executable": False,
        "reason_not_executable": (
            "Complete raw reasoning text was not preserved."
        ),
    }

    result = evaluate_reproduction_case(case)

    assert result["status"] == "DOCUMENTED"
    assert result["executed"] is False
    assert result["expectation_met"] is None


def test_fact_001_known_omission_is_detected() -> None:
    case = {
        "case_id": "REPRO-004",
        "evaluation_id": "FACT-001",
        "executable": True,
        "expected_evaluator_passed": False,
        "response": (
            "You can return most items within 30 days as long as "
            "they are unused and in original packaging."
        ),
        "reviewed_assertions": [
            {
                "fact_id": "return_window",
                "required": True,
                "accepted_patterns": ["30 days"],
            },
            {
                "fact_id": "unused_condition",
                "required": True,
                "accepted_patterns": ["unused"],
            },
            {
                "fact_id": "original_packaging_condition",
                "required": True,
                "accepted_patterns": ["original packaging"],
            },
            {
                "fact_id": "defective_item_exception",
                "required": True,
                "accepted_patterns": [
                    "defective",
                    "damaged",
                    "faulty",
                ],
            },
        ],
    }

    result = evaluate_reproduction_case(case)

    assert result["status"] == "DETECTED"
    assert result["expectation_met"] is True
    assert result["evaluator_passed"] is False
    assert result["evidence"]["missing_facts"] == [
        "defective_item_exception"
    ]


def test_unexpected_evaluator_result_is_reported_as_mismatch() -> None:
    case = {
        "case_id": "REPRO-TEST",
        "evaluation_id": "INV-012",
        "executable": True,
        "expected_evaluator_passed": False,
        "response": "Please contact our customer support team.",
    }

    result = evaluate_reproduction_case(case)

    assert result["status"] == "MISMATCH"
    assert result["expectation_met"] is False
    assert result["evaluator_passed"] is True