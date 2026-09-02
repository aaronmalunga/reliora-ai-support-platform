"""Unit tests for safe bug-ticket application orchestration."""

from datetime import UTC, datetime
from uuid import UUID

from reliora.domain.bug import BugReportDraft
from reliora.domain.operations import BugReportOperation
from reliora.domain.tickets import TicketCreationConfirmation
from reliora.policy.authorization import AuthorizationPreconditionStatus
from reliora.reliability.idempotency import InMemoryIdempotencyRegistry
from reliora.reliability.ticket_results import InMemoryTicketResultStore
from reliora.services.bug_ticket_application import BugTicketApplicationService
from reliora.services.ticket_execution import (
    TicketExecutionCoordinator,
    TicketExecutionStatus,
)

OPERATION_ID = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
SESSION_ID = UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")


class RecordingTicketProvider:
    """Deterministic ticket provider that records execution count."""

    def __init__(self) -> None:
        self.call_count = 0

    def create_bug_ticket(
        self,
        operation: BugReportOperation,
    ) -> TicketCreationConfirmation:
        """Return deterministic authoritative confirmation."""

        self.call_count += 1

        return TicketCreationConfirmation(
            operation_id=operation.operation_id,
            ticket_id="BUG-12345",
            provider="recording-ticket-provider",
            confirmed_at=datetime(2026, 9, 2, 16, 0, tzinfo=UTC),
        )


def service(
    provider: RecordingTicketProvider,
) -> BugTicketApplicationService:
    """Return an isolated application service."""

    coordinator = TicketExecutionCoordinator(
        idempotency_registry=InMemoryIdempotencyRegistry(),
        result_store=InMemoryTicketResultStore(),
        ticket_provider=provider,
    )

    return BugTicketApplicationService(
        ticket_execution=coordinator,
    )


def complete_operation(
    *,
    request_id: UUID,
    environment: str = "Chrome 120 on macOS Sonoma.",
) -> BugReportOperation:
    """Return a complete logical ticket operation."""

    return BugReportOperation(
        operation_id=OPERATION_ID,
        request_id=request_id,
        session_id=SESSION_ID,
        bug_report=BugReportDraft(
            description="Checkout crashes when Pay is clicked.",
            steps_to_reproduce="Open checkout and click Pay.",
            environment=environment,
        ),
    )


def test_incomplete_bug_is_denied_before_provider_execution() -> None:
    """FR-009/INV-003: incomplete bug data cannot reach ticket execution."""

    provider = RecordingTicketProvider()
    application = service(provider)

    operation = BugReportOperation(
        operation_id=OPERATION_ID,
        request_id=UUID(
            "11111111-1111-4111-8111-111111111111"
        ),
        session_id=SESSION_ID,
        bug_report=BugReportDraft(
            description="Checkout crashes.",
        ),
    )

    result = application.submit(operation)

    assert (
        result.authorization.status
        is AuthorizationPreconditionStatus.DENIED
    )
    assert result.execution is None
    assert provider.call_count == 0


def test_complete_bug_can_reach_authorized_execution_path() -> None:
    """FR-009/FR-013: validated bug data may reach confirmed execution."""

    provider = RecordingTicketProvider()
    application = service(provider)

    result = application.submit(
        complete_operation(
            request_id=UUID(
                "11111111-1111-4111-8111-111111111111"
            )
        )
    )

    assert (
        result.authorization.status
        is AuthorizationPreconditionStatus.READY_FOR_IDEMPOTENCY_CHECK
    )
    assert result.execution is not None
    assert result.execution.status is TicketExecutionStatus.CREATED
    assert result.execution.confirmation is not None
    assert provider.call_count == 1


def test_matching_retry_is_replayed_without_second_provider_call() -> None:
    """FR-011/INV-007: authorized retries preserve exactly-once execution."""

    provider = RecordingTicketProvider()
    application = service(provider)

    first = application.submit(
        complete_operation(
            request_id=UUID(
                "11111111-1111-4111-8111-111111111111"
            )
        )
    )
    retry = application.submit(
        complete_operation(
            request_id=UUID(
                "22222222-2222-4222-8222-222222222222"
            )
        )
    )

    assert first.execution is not None
    assert retry.execution is not None
    assert first.execution.status is TicketExecutionStatus.CREATED
    assert retry.execution.status is TicketExecutionStatus.REPLAYED
    assert retry.execution.confirmation == first.execution.confirmation
    assert provider.call_count == 1


def test_conflicting_retry_is_blocked_after_authorization() -> None:
    """FR-012/INV-008: authorized input still cannot bypass idempotency."""

    provider = RecordingTicketProvider()
    application = service(provider)

    first = application.submit(
        complete_operation(
            request_id=UUID(
                "11111111-1111-4111-8111-111111111111"
            )
        )
    )
    conflict = application.submit(
        complete_operation(
            request_id=UUID(
                "22222222-2222-4222-8222-222222222222"
            ),
            environment="Firefox on Windows 11.",
        )
    )

    assert first.execution is not None
    assert conflict.execution is not None
    assert first.execution.status is TicketExecutionStatus.CREATED
    assert conflict.execution.status is TicketExecutionStatus.CONFLICT
    assert conflict.execution.confirmation is None
    assert provider.call_count == 1


def test_denied_operation_does_not_consume_operation_identity() -> None:
    """FR-009/FR-010: denial must not register an unexecuted side effect."""

    provider = RecordingTicketProvider()
    application = service(provider)

    incomplete = BugReportOperation(
        operation_id=OPERATION_ID,
        request_id=UUID(
            "11111111-1111-4111-8111-111111111111"
        ),
        session_id=SESSION_ID,
        bug_report=BugReportDraft(
            description="Checkout crashes.",
        ),
    )

    denied = application.submit(incomplete)

    corrected = application.submit(
        complete_operation(
            request_id=UUID(
                "22222222-2222-4222-8222-222222222222"
            )
        )
    )

    assert (
        denied.authorization.status
        is AuthorizationPreconditionStatus.DENIED
    )
    assert denied.execution is None

    assert corrected.execution is not None
    assert corrected.execution.status is TicketExecutionStatus.CREATED
    assert provider.call_count == 1