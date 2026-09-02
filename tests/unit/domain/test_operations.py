"""Unit tests for Reliora side-effect operation contracts."""

from uuid import UUID

import pytest
from pydantic import ValidationError

from reliora.domain.bug import BugReportDraft
from reliora.domain.operations import BugReportOperation


def test_bug_report_operation_generates_operation_id() -> None:
    """FR-003: a new logical side effect receives an operation identifier."""

    operation = BugReportOperation(
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=UUID("22222222-2222-4222-8222-222222222222"),
        bug_report=BugReportDraft(description="Checkout crashes."),
    )

    assert isinstance(operation.operation_id, UUID)


def test_explicit_operation_id_is_preserved() -> None:
    """FR-003: callers can preserve logical operation identity across retries."""

    operation_id = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")

    operation = BugReportOperation(
        operation_id=operation_id,
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=UUID("22222222-2222-4222-8222-222222222222"),
        bug_report=BugReportDraft(description="Checkout crashes."),
    )

    assert operation.operation_id == operation_id


def test_same_operation_can_use_different_request_ids_across_retries() -> None:
    """FR-003: logical operation identity is independent of request attempts."""

    operation_id = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
    session_id = UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")

    first_attempt = BugReportOperation(
        operation_id=operation_id,
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=session_id,
        bug_report=BugReportDraft(description="Checkout crashes."),
    )
    retry_attempt = BugReportOperation(
        operation_id=operation_id,
        request_id=UUID("22222222-2222-4222-8222-222222222222"),
        session_id=session_id,
        bug_report=BugReportDraft(description="Checkout crashes."),
    )

    assert first_attempt.operation_id == retry_attempt.operation_id
    assert first_attempt.request_id != retry_attempt.request_id
    assert first_attempt.session_id == retry_attempt.session_id


def test_operation_accepts_incomplete_bug_report_as_proposal() -> None:
    """FR-007/FR-009: proposal state remains separate from authorization."""

    operation = BugReportOperation(
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=UUID("22222222-2222-4222-8222-222222222222"),
        bug_report=BugReportDraft(description="Checkout crashes."),
    )

    assert operation.bug_report.is_complete is False


def test_operation_accepts_complete_bug_report() -> None:
    """A fully collected bug report can cross into the authorization boundary."""

    bug_report = BugReportDraft(
        description="Checkout crashes when Pay is clicked.",
        steps_to_reproduce="Open checkout and click Pay.",
        environment="Chrome 120 on macOS Sonoma.",
    )

    operation = BugReportOperation(
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=UUID("22222222-2222-4222-8222-222222222222"),
        bug_report=bug_report,
    )

    assert operation.bug_report == bug_report
    assert operation.bug_report.is_complete is True


def test_raw_nested_bug_report_is_validated_into_domain_contract() -> None:
    """FR-019: raw operation data must cross typed validation boundaries."""

    operation = BugReportOperation.model_validate(
        {
            "request_id": "11111111-1111-4111-8111-111111111111",
            "session_id": "22222222-2222-4222-8222-222222222222",
            "bug_report": {
                "description": "Checkout crashes.",
                "steps_to_reproduce": "Click Pay.",
                "environment": "Chrome on Windows 11.",
            },
        }
    )

    assert isinstance(operation.request_id, UUID)
    assert isinstance(operation.session_id, UUID)
    assert isinstance(operation.bug_report, BugReportDraft)


def test_operation_rejects_unexpected_fields() -> None:
    """FR-019/FR-020: undeclared operation data cannot enter the contract."""

    with pytest.raises(ValidationError):
        BugReportOperation.model_validate(
            {
                "request_id": "11111111-1111-4111-8111-111111111111",
                "session_id": "22222222-2222-4222-8222-222222222222",
                "bug_report": {
                    "description": "Checkout crashes.",
                },
                "authorized": True,
            }
        )


def test_operation_is_immutable_after_validation() -> None:
    """Stable operation identity cannot be silently changed after validation."""

    operation = BugReportOperation(
        operation_id=UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=UUID("22222222-2222-4222-8222-222222222222"),
        bug_report=BugReportDraft(description="Checkout crashes."),
    )

    with pytest.raises(ValidationError):
        operation.operation_id = UUID("cccccccc-cccc-4ccc-8ccc-cccccccccccc")