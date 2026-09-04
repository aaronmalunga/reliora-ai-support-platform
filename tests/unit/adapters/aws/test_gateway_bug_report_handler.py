"""Tests for the composed AgentCore Gateway bug-ticket workflow."""

from datetime import UTC, datetime
from uuid import UUID

from reliora.adapters.aws.gateway_bug_report_handler import (
    GatewayBugReportHandler,
)
from reliora.adapters.aws.gateway_bug_report_operation import (
    TrustedOperationIdentity,
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
CONFIRMED_AT = datetime(2026, 9, 3, 20, 0, tzinfo=UTC)


class RecordingTicketExecution:
    """Record submitted operations while returning a confirmed ticket."""

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


def _identity() -> TrustedOperationIdentity:
    return TrustedOperationIdentity(
        operation_id=OPERATION_ID,
        request_id=REQUEST_ID,
        session_id=SESSION_ID,
    )


def _gateway_event() -> dict[str, str]:
    return {
        "description": "Checkout crashes",
        "stepsToReproduce": "Open cart, then click Pay",
        "environment": "Chrome 120 on macOS",
    }


def test_gateway_handler_composes_successful_ticket_workflow() -> None:
    execution = RecordingTicketExecution()
    handler = GatewayBugReportHandler(
        ticket_execution=execution,
    )

    response = handler.handle(
        _gateway_event(),
        identity=_identity(),
    )

    assert response == {
        "status": "OPEN",
        "ticketId": "BUG-123",
        "executionStatus": "CREATED",
    }

    assert len(execution.operations) == 1

    operation = execution.operations[0]

    assert operation.operation_id == OPERATION_ID
    assert operation.request_id == REQUEST_ID
    assert operation.session_id == SESSION_ID
    assert operation.bug_report.description == "Checkout crashes"
    assert operation.bug_report.steps_to_reproduce == (
        "Open cart, then click Pay"
    )
    assert operation.bug_report.environment == "Chrome 120 on macOS"


def test_gateway_handler_denial_stops_before_ticket_execution() -> None:
    execution = RecordingTicketExecution()
    handler = GatewayBugReportHandler(
        ticket_execution=execution,
    )

    event = _gateway_event()
    event["environment"] = "   "

    response = handler.handle(
        event,
        identity=_identity(),
    )

    assert response == {
        "status": "REJECTED",
        "errorCode": "INCOMPLETE_BUG_REPORT",
        "missingFields": ["environment"],
    }

    assert execution.operations == []