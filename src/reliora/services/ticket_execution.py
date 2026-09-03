"""Safe execution coordinator for bug-ticket side effects."""

from enum import StrEnum
from typing import Protocol
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from reliora.domain.operations import BugReportOperation
from reliora.domain.tickets import TicketCreationConfirmation
from reliora.providers.tickets import TicketProvider
from reliora.reliability.idempotency import (
    IdempotencyStatus,
    InMemoryIdempotencyRegistry,
)
from reliora.reliability.ticket_results import InMemoryTicketResultStore


class TicketExecutionStatus(StrEnum):
    """Deterministic outcome of attempting a logical ticket operation."""

    CREATED = "CREATED"
    REPLAYED = "REPLAYED"
    CONFLICT = "CONFLICT"
    UNCONFIRMED = "UNCONFIRMED"


class TicketExecutionResult(BaseModel):
    """Application-level result of ticket execution coordination."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    operation_id: UUID
    request_id: UUID
    status: TicketExecutionStatus
    confirmation: TicketCreationConfirmation | None = None


class TicketExecutionPort(Protocol):
    """Port for executing one authorized logical ticket operation."""

    def execute(
        self,
        operation: BugReportOperation,
    ) -> TicketExecutionResult:
        """Execute, replay, or reject one logical ticket operation."""
        ...


class TicketExecutionCoordinator:
    """Coordinate idempotency, provider execution, and result replay."""

    def __init__(
        self,
        *,
        idempotency_registry: InMemoryIdempotencyRegistry,
        result_store: InMemoryTicketResultStore,
        ticket_provider: TicketProvider,
    ) -> None:
        self._idempotency_registry = idempotency_registry
        self._result_store = result_store
        self._ticket_provider = ticket_provider

    def execute(
        self,
        operation: BugReportOperation,
    ) -> TicketExecutionResult:
        """Safely execute or replay one logical ticket operation."""

        admission = self._idempotency_registry.check_and_register(operation)

        if admission.status is IdempotencyStatus.CONFLICT:
            return TicketExecutionResult(
                operation_id=operation.operation_id,
                request_id=operation.request_id,
                status=TicketExecutionStatus.CONFLICT,
            )

        existing_confirmation = self._result_store.get(
            operation.operation_id
        )

        if admission.status is IdempotencyStatus.MATCHING_OPERATION:
            if existing_confirmation is None:
                return TicketExecutionResult(
                    operation_id=operation.operation_id,
                    request_id=operation.request_id,
                    status=TicketExecutionStatus.UNCONFIRMED,
                )

            return TicketExecutionResult(
                operation_id=operation.operation_id,
                request_id=operation.request_id,
                status=TicketExecutionStatus.REPLAYED,
                confirmation=existing_confirmation,
            )

        confirmation = self._ticket_provider.create_bug_ticket(operation)

        if confirmation.operation_id != operation.operation_id:
            raise ValueError(
                "Ticket provider confirmation operation_id does not match "
                "the requested logical operation."
            )

        stored_confirmation = self._result_store.save(confirmation)

        return TicketExecutionResult(
            operation_id=operation.operation_id,
            request_id=operation.request_id,
            status=TicketExecutionStatus.CREATED,
            confirmation=stored_confirmation,
        )