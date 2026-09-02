"""Unit tests for Reliora idempotency controls."""

from uuid import UUID

from reliora.domain.bug import BugReportDraft
from reliora.domain.operations import BugReportOperation
from reliora.reliability.idempotency import (
    IdempotencyStatus,
    InMemoryIdempotencyRegistry,
    bug_report_fingerprint,
)


def complete_bug_report() -> BugReportDraft:
    """Return a complete normalized bug report for idempotency tests."""

    return BugReportDraft(
        description="Checkout crashes when Pay is clicked.",
        steps_to_reproduce="Open checkout and click Pay.",
        environment="Chrome 120 on macOS Sonoma.",
    )


def test_first_operation_is_registered_as_new() -> None:
    """FR-010: the first occurrence of a logical operation is new."""

    registry = InMemoryIdempotencyRegistry()
    operation = BugReportOperation(
        operation_id=UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=UUID("22222222-2222-4222-8222-222222222222"),
        bug_report=complete_bug_report(),
    )

    decision = registry.check_and_register(operation)

    assert decision.status is IdempotencyStatus.NEW_OPERATION
    assert decision.operation_id == operation.operation_id
    assert decision.request_id == operation.request_id


def test_same_operation_id_and_payload_is_matching_retry() -> None:
    """FR-011: the same logical operation can be recognized on retry."""

    registry = InMemoryIdempotencyRegistry()
    operation_id = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
    session_id = UUID("22222222-2222-4222-8222-222222222222")

    first_attempt = BugReportOperation(
        operation_id=operation_id,
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=session_id,
        bug_report=complete_bug_report(),
    )
    retry_attempt = BugReportOperation(
        operation_id=operation_id,
        request_id=UUID("33333333-3333-4333-8333-333333333333"),
        session_id=session_id,
        bug_report=complete_bug_report(),
    )

    first_decision = registry.check_and_register(first_attempt)
    retry_decision = registry.check_and_register(retry_attempt)

    assert first_decision.status is IdempotencyStatus.NEW_OPERATION
    assert retry_decision.status is IdempotencyStatus.MATCHING_OPERATION
    assert retry_decision.operation_id == operation_id
    assert retry_decision.request_id == retry_attempt.request_id


def test_same_operation_id_with_different_payload_is_conflict() -> None:
    """FR-012/H-008: changed operation data cannot reuse an existing identity."""

    registry = InMemoryIdempotencyRegistry()
    operation_id = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
    session_id = UUID("22222222-2222-4222-8222-222222222222")

    original = BugReportOperation(
        operation_id=operation_id,
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=session_id,
        bug_report=complete_bug_report(),
    )
    conflicting = BugReportOperation(
        operation_id=operation_id,
        request_id=UUID("33333333-3333-4333-8333-333333333333"),
        session_id=session_id,
        bug_report=BugReportDraft(
            description="Search page crashes instead.",
            steps_to_reproduce="Open search and submit a query.",
            environment="Firefox on Windows 11.",
        ),
    )

    registry.check_and_register(original)
    decision = registry.check_and_register(conflicting)

    assert decision.status is IdempotencyStatus.CONFLICT


def test_conflict_does_not_replace_original_registration() -> None:
    """FR-012: conflicting reuse cannot overwrite the original logical payload."""

    registry = InMemoryIdempotencyRegistry()
    operation_id = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
    session_id = UUID("22222222-2222-4222-8222-222222222222")

    original = BugReportOperation(
        operation_id=operation_id,
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=session_id,
        bug_report=complete_bug_report(),
    )
    conflicting = BugReportOperation(
        operation_id=operation_id,
        request_id=UUID("33333333-3333-4333-8333-333333333333"),
        session_id=session_id,
        bug_report=BugReportDraft(
            description="Search page crashes instead.",
            steps_to_reproduce="Open search and submit a query.",
            environment="Firefox on Windows 11.",
        ),
    )
    later_original_retry = BugReportOperation(
        operation_id=operation_id,
        request_id=UUID("44444444-4444-4444-8444-444444444444"),
        session_id=session_id,
        bug_report=complete_bug_report(),
    )

    registry.check_and_register(original)
    conflict_decision = registry.check_and_register(conflicting)
    retry_decision = registry.check_and_register(later_original_retry)

    assert conflict_decision.status is IdempotencyStatus.CONFLICT
    assert retry_decision.status is IdempotencyStatus.MATCHING_OPERATION


def test_different_operation_ids_are_independent() -> None:
    """FR-003/FR-010: distinct logical actions are admitted independently."""

    registry = InMemoryIdempotencyRegistry()
    session_id = UUID("22222222-2222-4222-8222-222222222222")

    first_operation = BugReportOperation(
        operation_id=UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=session_id,
        bug_report=complete_bug_report(),
    )
    second_operation = BugReportOperation(
        operation_id=UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"),
        request_id=UUID("33333333-3333-4333-8333-333333333333"),
        session_id=session_id,
        bug_report=complete_bug_report(),
    )

    first_decision = registry.check_and_register(first_operation)
    second_decision = registry.check_and_register(second_operation)

    assert first_decision.status is IdempotencyStatus.NEW_OPERATION
    assert second_decision.status is IdempotencyStatus.NEW_OPERATION


def test_fingerprint_is_deterministic_for_same_normalized_report() -> None:
    """Idempotency comparison remains stable for equivalent normalized input."""

    first = BugReportDraft(
        description="   Checkout crashes when Pay is clicked.   ",
        steps_to_reproduce="   Open checkout and click Pay.   ",
        environment="   Chrome 120 on macOS Sonoma.   ",
    )
    second = complete_bug_report()

    assert bug_report_fingerprint(first) == bug_report_fingerprint(second)


def test_material_payload_change_changes_fingerprint() -> None:
    """FR-012: materially different bug data receives a different fingerprint."""

    original = complete_bug_report()
    changed = BugReportDraft(
        description="Checkout crashes when Pay is clicked.",
        steps_to_reproduce="Open checkout and click Pay.",
        environment="Firefox on Windows 11.",
    )

    assert bug_report_fingerprint(original) != bug_report_fingerprint(changed)


def test_fingerprint_has_expected_sha256_shape() -> None:
    """Fingerprint representation is stable and machine-verifiable."""

    fingerprint = bug_report_fingerprint(complete_bug_report())

    assert len(fingerprint) == 64
    assert all(character in "0123456789abcdef" for character in fingerprint)