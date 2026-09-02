"""Unit tests for safe bug-ticket execution coordination."""

from datetime import UTC, datetime
from uuid import UUID

import pytest

from reliora.domain.bug import BugReportDraft
from reliora.domain.operations import BugReportOperation
from reliora.domain.tickets import TicketCreationConfirmation
from reliora.reliability.idempotency import InMemoryIdempotencyRegistry
from reliora.reliability.ticket_results import InMemoryTicketResultStore
from reliora.services.ticket_execution import (
    TicketExecutionCoordinator,
    TicketExecutionStatus,
)

OPERATION_ID = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
SESSION_ID = UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")


class FakeTicketProvider:
    """Deterministic provider double that records execution count."""

    def __init__(self) -> None:
        self.call_count = 0

    def create_bug_ticket(
        self,
        operation: BugReportOperation,
    ) -> TicketCreationConfirmation:
        """Return authoritative-looking confirmation for test execution."""

        self.call_count += 1

        return TicketCreationConfirmation(
            operation_id=operation.operation_id,
            ticket_id="BUG-12345",
            provider="fake-ticket-provider",
            confirmed_at=datetime(2026, 9, 2, 16, 0, tzinfo=UTC),
        )


class WrongOperationTicketProvider:
    """Provider double that returns confirmation for the wrong operation."""

    def create_bug_ticket(
        self,
        operation: BugReportOperation,
    ) -> TicketCreationConfirmation:
        """Return deliberately invalid operation provenance."""

        return TicketCreationConfirmation(
            operation_id=UUID(
                "cccccccc-cccc-4ccc-8ccc-cccccccccccc"
            ),
            ticket_id="BUG-99999",
            provider="wrong-operation-provider",
            confirmed_at=datetime(2026, 9, 2, 16, 0, tzinfo=UTC),
        )


def bug_report(
    *,
    environment: str = "Chrome 120 on macOS Sonoma.",
) -> BugReportDraft:
    """Return a complete bug report."""

    return BugReportDraft(
        description="Checkout crashes when Pay is clicked.",
        steps_to_reproduce="Open checkout and click Pay.",
        environment=environment,
    )


def operation(
    *,
    request_id: UUID,
    environment: str = "Chrome 120 on macOS Sonoma.",
) -> BugReportOperation:
    """Return one logical ticket operation."""

    return BugReportOperation(
        operation_id=OPERATION_ID,
        request_id=request_id,
        session_id=SESSION_ID,
        bug_report=bug_report(environment=environment),
    )


def coordinator(
    provider: FakeTicketProvider,
) -> TicketExecutionCoordinator:
    """Return a coordinator with isolated in-memory dependencies."""

    return TicketExecutionCoordinator(
        idempotency_registry=InMemoryIdempotencyRegistry(),
        result_store=InMemoryTicketResultStore(),
        ticket_provider=provider,
    )


def test_new_operation_executes_provider_and_returns_confirmation() -> None:
    """FR-013/INV-009: new execution requires backend confirmation."""

    provider = FakeTicketProvider()
    service = coordinator(provider)

    result = service.execute(
        operation(
            request_id=UUID(
                "11111111-1111-4111-8111-111111111111"
            )
        )
    )

    assert result.status is TicketExecutionStatus.CREATED
    assert result.confirmation is not None
    assert result.confirmation.ticket_id == "BUG-12345"
    assert provider.call_count == 1


def test_matching_retry_replays_result_without_provider_execution() -> None:
    """FR-011/INV-007: matching retry does not create another ticket."""

    provider = FakeTicketProvider()
    service = coordinator(provider)

    first_result = service.execute(
        operation(
            request_id=UUID(
                "11111111-1111-4111-8111-111111111111"
            )
        )
    )
    retry_result = service.execute(
        operation(
            request_id=UUID(
                "22222222-2222-4222-8222-222222222222"
            )
        )
    )

    assert first_result.status is TicketExecutionStatus.CREATED
    assert retry_result.status is TicketExecutionStatus.REPLAYED
    assert retry_result.confirmation == first_result.confirmation
    assert provider.call_count == 1


def test_conflicting_retry_is_blocked_without_provider_execution() -> None:
    """FR-012/INV-008: conflicting payload reuse cannot execute."""

    provider = FakeTicketProvider()
    service = coordinator(provider)

    original = operation(
        request_id=UUID(
            "11111111-1111-4111-8111-111111111111"
        )
    )
    conflicting = operation(
        request_id=UUID(
            "22222222-2222-4222-8222-222222222222"
        ),
        environment="Firefox on Windows 11.",
    )

    first_result = service.execute(original)
    conflict_result = service.execute(conflicting)

    assert first_result.status is TicketExecutionStatus.CREATED
    assert conflict_result.status is TicketExecutionStatus.CONFLICT
    assert conflict_result.confirmation is None
    assert provider.call_count == 1


def test_matching_registered_operation_without_result_is_unconfirmed() -> None:
    """H-007: known operation without confirmation must not be guessed."""

    registry = InMemoryIdempotencyRegistry()
    result_store = InMemoryTicketResultStore()
    provider = FakeTicketProvider()

    original = operation(
        request_id=UUID(
            "11111111-1111-4111-8111-111111111111"
        )
    )
    registry.check_and_register(original)

    service = TicketExecutionCoordinator(
        idempotency_registry=registry,
        result_store=result_store,
        ticket_provider=provider,
    )

    retry = operation(
        request_id=UUID(
            "22222222-2222-4222-8222-222222222222"
        )
    )

    result = service.execute(retry)

    assert result.status is TicketExecutionStatus.UNCONFIRMED
    assert result.confirmation is None
    assert provider.call_count == 0


def test_provider_confirmation_must_match_operation_identity() -> None:
    """FR-013/INV-010: backend evidence must bind to the requested operation."""

    service = TicketExecutionCoordinator(
        idempotency_registry=InMemoryIdempotencyRegistry(),
        result_store=InMemoryTicketResultStore(),
        ticket_provider=WrongOperationTicketProvider(),
    )

    with pytest.raises(
        ValueError,
        match="confirmation operation_id does not match",
    ):
        service.execute(
            operation(
                request_id=UUID(
                    "11111111-1111-4111-8111-111111111111"
                )
            )
        )