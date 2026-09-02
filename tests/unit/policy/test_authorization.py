"""Unit tests for Reliora deterministic authorization preconditions."""

from uuid import UUID

import pytest
from pydantic import ValidationError

from reliora.domain.bug import BugField, BugReportDraft
from reliora.domain.operations import BugReportOperation
from reliora.policy.authorization import (
    AuthorizationPreconditionDecision,
    AuthorizationPreconditionStatus,
    AuthorizationReason,
    evaluate_bug_report_preconditions,
)


def test_incomplete_bug_report_is_denied() -> None:
    """FR-007/FR-009: incomplete bug information cannot proceed toward execution."""

    operation = BugReportOperation(
        operation_id=UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=UUID("22222222-2222-4222-8222-222222222222"),
        bug_report=BugReportDraft(
            description="Checkout crashes when Pay is clicked.",
        ),
    )

    decision = evaluate_bug_report_preconditions(operation)

    assert decision.status is AuthorizationPreconditionStatus.DENIED
    assert decision.reason is AuthorizationReason.INCOMPLETE_BUG_REPORT


def test_denial_preserves_exact_missing_fields() -> None:
    """FR-007/FR-008: denial evidence identifies the unmet required fields."""

    operation = BugReportOperation(
        operation_id=UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=UUID("22222222-2222-4222-8222-222222222222"),
        bug_report=BugReportDraft(
            description="Checkout crashes.",
        ),
    )

    decision = evaluate_bug_report_preconditions(operation)

    assert decision.missing_fields == (
        BugField.STEPS_TO_REPRODUCE,
        BugField.ENVIRONMENT,
    )


def test_complete_bug_report_is_ready_for_idempotency_check() -> None:
    """FR-009: complete validated data may advance to the next control boundary."""

    operation = BugReportOperation(
        operation_id=UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=UUID("22222222-2222-4222-8222-222222222222"),
        bug_report=BugReportDraft(
            description="Checkout crashes when Pay is clicked.",
            steps_to_reproduce="Open checkout and click Pay.",
            environment="Chrome 120 on macOS Sonoma.",
        ),
    )

    decision = evaluate_bug_report_preconditions(operation)

    assert (
        decision.status
        is AuthorizationPreconditionStatus.READY_FOR_IDEMPOTENCY_CHECK
    )
    assert decision.reason is AuthorizationReason.PRECONDITIONS_SATISFIED
    assert decision.missing_fields == ()


def test_decision_propagates_request_and_operation_identifiers() -> None:
    """FR-003/FR-028: authorization evidence remains correlated to its operation."""

    operation_id = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
    request_id = UUID("11111111-1111-4111-8111-111111111111")

    operation = BugReportOperation(
        operation_id=operation_id,
        request_id=request_id,
        session_id=UUID("22222222-2222-4222-8222-222222222222"),
        bug_report=BugReportDraft(
            description="Checkout crashes.",
        ),
    )

    decision = evaluate_bug_report_preconditions(operation)

    assert decision.operation_id == operation_id
    assert decision.request_id == request_id


@pytest.mark.parametrize(
    ("missing_field", "expected"),
    [
        ("description", BugField.DESCRIPTION),
        ("steps_to_reproduce", BugField.STEPS_TO_REPRODUCE),
        ("environment", BugField.ENVIRONMENT),
    ],
)
def test_each_required_bug_field_can_independently_block_progress(
    missing_field: str,
    expected: BugField,
) -> None:
    """FR-007/FR-009: every required field is independently enforced."""


    raw_bug_report: dict[str, str | None] = {
        "description": "Checkout crashes.",
        "steps_to_reproduce": "Click Pay.",
        "environment": "Chrome on Windows 11.",
    }



    raw_bug_report[missing_field] = None

    operation = BugReportOperation.model_validate(
        {
            "operation_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
            "request_id": "11111111-1111-4111-8111-111111111111",
            "session_id": "22222222-2222-4222-8222-222222222222",
            "bug_report": raw_bug_report,
      }
  )

    decision = evaluate_bug_report_preconditions(operation)

    assert decision.status is AuthorizationPreconditionStatus.DENIED
    assert decision.missing_fields == (expected,)


def test_authorization_precondition_decision_is_immutable() -> None:
    """A deterministic authorization record cannot be silently rewritten."""

    decision = AuthorizationPreconditionDecision(
        operation_id=UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        status=AuthorizationPreconditionStatus.DENIED,
        reason=AuthorizationReason.INCOMPLETE_BUG_REPORT,
        missing_fields=(BugField.ENVIRONMENT,),
    )

    with pytest.raises(ValidationError):
        decision.status = AuthorizationPreconditionStatus.READY_FOR_IDEMPOTENCY_CHECK


def test_authorization_decision_rejects_injected_execution_claim() -> None:
    """AP-003: callers cannot add execution authorization outside the contract."""

    with pytest.raises(ValidationError):
        AuthorizationPreconditionDecision.model_validate(
            {
                "operation_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
                "request_id": "11111111-1111-4111-8111-111111111111",
                "status": "READY_FOR_IDEMPOTENCY_CHECK",
                "reason": "PRECONDITIONS_SATISFIED",
                "missing_fields": [],
                "authorized": True,
            }
        )