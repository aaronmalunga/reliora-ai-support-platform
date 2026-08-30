"""Unit tests for deterministic bug-workflow evaluation."""

from reliora.evaluation.bug_workflow import (
    BugField,
    evaluate_incremental_bug_collection,
)


def test_one_requested_missing_field_passes() -> None:
    result = evaluate_incremental_bug_collection(
        missing_fields=[
            BugField.STEPS_TO_REPRODUCE,
            BugField.ENVIRONMENT,
        ],
        requested_fields=[BugField.STEPS_TO_REPRODUCE],
    )

    assert result.passed is True
    assert result.invariant_id == "INV-004"


def test_different_single_missing_field_can_be_requested() -> None:
    result = evaluate_incremental_bug_collection(
        missing_fields=[
            BugField.STEPS_TO_REPRODUCE,
            BugField.ENVIRONMENT,
        ],
        requested_fields=[BugField.ENVIRONMENT],
    )

    assert result.passed is True


def test_multiple_requested_missing_fields_fail() -> None:
    result = evaluate_incremental_bug_collection(
        missing_fields=[
            BugField.STEPS_TO_REPRODUCE,
            BugField.ENVIRONMENT,
        ],
        requested_fields=[
            BugField.STEPS_TO_REPRODUCE,
            BugField.ENVIRONMENT,
        ],
    )

    assert result.passed is False
    assert result.evidence["requested_fields"] == [
        "steps_to_reproduce",
        "environment",
    ]


def test_requesting_non_missing_field_fails() -> None:
    result = evaluate_incremental_bug_collection(
        missing_fields=[BugField.ENVIRONMENT],
        requested_fields=[BugField.DESCRIPTION],
    )

    assert result.passed is False
    assert result.evidence["invalid_requested_fields"] == ["description"]


def test_no_missing_fields_and_no_request_passes() -> None:
    result = evaluate_incremental_bug_collection(
        missing_fields=[],
        requested_fields=[],
    )

    assert result.passed is True


def test_requesting_field_when_nothing_is_missing_fails() -> None:
    result = evaluate_incremental_bug_collection(
        missing_fields=[],
        requested_fields=[BugField.ENVIRONMENT],
    )

    assert result.passed is False