"""Tests for the Reliora Lambda-style bug-report runtime."""

from datetime import UTC, datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from reliora.adapters.aws.gateway_bug_report_operation import (
    TrustedOperationIdentity,
)
from reliora.adapters.aws.lambda_bug_report_runtime import (
    LambdaBugReportRuntime,
)
from reliora.domain.operations import BugReportOperation
from reliora.domain.tickets import TicketCreationConfirmation
from reliora.services.ticket_execution import (
    TicketExecutionResult,
    TicketExecutionStatus,
)

OPERATION_ID = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
REQUEST_ID = UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")
SESSION_ID = UUID("cccccccc-cccc-4ccc-8ccc-cccccccccccc")
CONFIRMED_AT = datetime(2026, 9, 4, 5, 0, tzinfo=UTC)


class FakeLambdaContext:
    """Small stand-in for runtime-owned Lambda context."""



class RecordingIdentityResolver:
    """Return deterministic trusted identity and record the supplied context."""

    def __init__(self) -> None:
        self.contexts: list[object] = []

    def resolve(
        self,
        context: object,
    ) -> TrustedOperationIdentity:
        self.contexts.append(context)

        return TrustedOperationIdentity(
            operation_id=OPERATION_ID,
            request_id=REQUEST_ID,
            session_id=SESSION_ID,
        )


class RecordingTicketExecution:
    """Record execution and return an authoritative confirmation."""

    def __init__(self) -> None:
        self.operations: list[BugReportOperation] = []

    def execute(
        self,
        operation: BugReportOperation,
    ) -> TicketExecutionResult:
        self.operations.append(operation)

        return TicketExecutionResult(
            operation_id=operation.operation_id,
            request_id=operation.request_id,
            status=TicketExecutionStatus.CREATED,
            confirmation=TicketCreationConfirmation(
                operation_id=operation.operation_id,
                ticket_id="BUG-123",
                provider="test-provider",
                confirmed_at=CONFIRMED_AT,
            ),
        )


def test_lambda_runtime_composes_context_identity_and_gateway_event() -> None:
    context = FakeLambdaContext()
    identity_resolver = RecordingIdentityResolver()
    execution = RecordingTicketExecution()

    runtime = LambdaBugReportRuntime(
        ticket_execution=execution,
        identity_resolver=identity_resolver,
    )

    response = runtime.handle(
        {
            "description": "Checkout crashes",
            "stepsToReproduce": "Open cart, then click Pay",
            "environment": "Chrome 120 on macOS",
        },
        context,
    )

    assert response == {
        "status": "OPEN",
        "ticketId": "BUG-123",
        "executionStatus": "CREATED",
    }

    assert identity_resolver.contexts == [context]
    assert len(execution.operations) == 1

    operation = execution.operations[0]

    assert operation.operation_id == OPERATION_ID
    assert operation.request_id == REQUEST_ID
    assert operation.session_id == SESSION_ID


def test_lambda_runtime_does_not_take_identity_from_tool_event() -> None:
    context = FakeLambdaContext()
    identity_resolver = RecordingIdentityResolver()
    execution = RecordingTicketExecution()

    runtime = LambdaBugReportRuntime(
        ticket_execution=execution,
        identity_resolver=identity_resolver,
    )

    event = {
        "description": "Checkout crashes",
        "stepsToReproduce": "Open cart, then click Pay",
        "environment": "Chrome 120 on macOS",
        "operation_id": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
    }

    with pytest.raises(ValidationError):
        runtime.handle(event, context)

    assert execution.operations == []