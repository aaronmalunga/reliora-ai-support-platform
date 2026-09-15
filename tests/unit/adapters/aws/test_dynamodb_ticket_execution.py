"""Unit tests for durable DynamoDB ticket execution."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

import pytest
from botocore.exceptions import ClientError, ReadTimeoutError

from reliora.adapters.aws.dynamodb_ticket_execution import (
    DynamoDBTicketExecutionCoordinator,
)
from reliora.domain.bug import BugReportDraft
from reliora.domain.operations import BugReportOperation
from reliora.reliability.idempotency import bug_report_fingerprint
from reliora.services.ticket_execution import TicketExecutionStatus
from reliora.telemetry.failures import FailureCategory, FailureEvent

OPERATION_ID = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
SESSION_ID = UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")
FIRST_REQUEST_ID = UUID("11111111-1111-4111-8111-111111111111")
RETRY_REQUEST_ID = UUID("22222222-2222-4222-8222-222222222222")

CONFIRMED_AT = datetime(2026, 9, 3, 15, 30, tzinfo=UTC)
TICKET_ID = "BUG-12345"

OPERATIONS_TABLE = "reliora-dev-operations"
TICKETS_TABLE = "reliora-dev-tickets"


class FakeDynamoDBClient:
    """Deterministic DynamoDB double for execution-adapter tests."""

    def __init__(
        self,
        *,
        get_item_responses: list[dict[str, Any]] | None = None,
        transaction_error: Exception | None = None,
    ) -> None:
        self.get_item_responses = list(get_item_responses or [])
        self.transaction_error = transaction_error
        self.get_item_calls: list[dict[str, Any]] = []
        self.transaction_calls: list[dict[str, Any]] = []

    def get_item(self, **kwargs: Any) -> dict[str, Any]:
        """Record one read and return the next configured response."""

        self.get_item_calls.append(kwargs)

        if self.get_item_responses:
            return self.get_item_responses.pop(0)

        return {}

    def transact_write_items(self, **kwargs: Any) -> dict[str, Any]:
        """Record one transaction and optionally raise an AWS error."""

        self.transaction_calls.append(kwargs)

        if self.transaction_error is not None:
            raise self.transaction_error

        return {}


class RecordingFailureTelemetrySink:
    """Record failure events emitted by the adapter."""

    def __init__(self) -> None:
        self.events: list[FailureEvent] = []

    def record(self, event: FailureEvent) -> None:
        self.events.append(event)


class FailingFailureTelemetrySink:
    """Simulate an unavailable telemetry destination."""

    def record(self, event: FailureEvent) -> None:
        raise RuntimeError("Telemetry unavailable.")


def complete_bug_report(
    *,
    environment: str = "Chrome 120 on macOS Sonoma.",
) -> BugReportDraft:
    """Return one complete bug report."""

    return BugReportDraft(
        description="Checkout crashes when Pay is clicked.",
        steps_to_reproduce="Open checkout and click Pay.",
        environment=environment,
    )


def operation(
    *,
    request_id: UUID = FIRST_REQUEST_ID,
    environment: str = "Chrome 120 on macOS Sonoma.",
) -> BugReportOperation:
    """Return one logical bug-ticket operation."""

    return BugReportOperation(
        operation_id=OPERATION_ID,
        request_id=request_id,
        session_id=SESSION_ID,
        bug_report=complete_bug_report(environment=environment),
    )


def stored_operation_item(
    *,
    environment: str = "Chrome 120 on macOS Sonoma.",
) -> dict[str, Any]:
    """Return a complete authoritative DynamoDB operation item."""

    fingerprint = bug_report_fingerprint(
        complete_bug_report(environment=environment)
    )

    return {
        "Item": {
            "operation_id": {
                "S": str(OPERATION_ID),
            },
            "payload_fingerprint": {
                "S": fingerprint,
            },
            "ticket_id": {
                "S": TICKET_ID,
            },
            "provider": {
                "S": "reliora-dynamodb",
            },
            "confirmed_at": {
                "S": CONFIRMED_AT.isoformat(),
            },
        }
    }

def transaction_cancelled_error() -> ClientError:
    """Return the AWS error used when a transaction is cancelled."""

    return ClientError(
        {
            "Error": {
                "Code": "TransactionCanceledException",
                "Message": "Transaction cancelled.",
            }
        },
        "TransactWriteItems",
    )


def access_denied_error() -> ClientError:
    """Return a non-ambiguous AWS service error that must propagate."""

    return ClientError(
        {
            "Error": {
                "Code": "AccessDeniedException",
                "Message": "Access denied.",
            }
        },
        "TransactWriteItems",
    )


def read_timeout_error() -> ReadTimeoutError:
    """Return an ambiguous transport timeout after a DynamoDB request."""

    return ReadTimeoutError(
        endpoint_url="https://dynamodb.us-east-1.amazonaws.com"
    )

def coordinator(
    client: FakeDynamoDBClient,
) -> DynamoDBTicketExecutionCoordinator:
    """Return a deterministic DynamoDB execution coordinator."""

    return DynamoDBTicketExecutionCoordinator(
        dynamodb_client=client,
        operations_table_name=OPERATIONS_TABLE,
        tickets_table_name=TICKETS_TABLE,
        ticket_id_factory=lambda: TICKET_ID,
        clock=lambda: CONFIRMED_AT,
    )


def test_new_operation_atomically_creates_operation_and_ticket() -> None:
    """ADR-016/FR-013: one transaction persists both authoritative records."""

    client = FakeDynamoDBClient(
        get_item_responses=[{}],
    )
    service = coordinator(client)

    result = service.execute(operation())

    assert result.status is TicketExecutionStatus.CREATED
    assert result.confirmation is not None
    assert result.confirmation.ticket_id == TICKET_ID

    assert len(client.transaction_calls) == 1

    transaction = client.transaction_calls[0]
    items = transaction["TransactItems"]

    assert len(items) == 2

    operation_put = items[0]["Put"]
    ticket_put = items[1]["Put"]

    assert operation_put["TableName"] == OPERATIONS_TABLE
    assert (
        operation_put["ConditionExpression"]
        == "attribute_not_exists(operation_id)"
    )

    assert ticket_put["TableName"] == TICKETS_TABLE
    assert (
        ticket_put["ConditionExpression"]
        == "attribute_not_exists(ticket_id)"
    )

    assert (
        operation_put["Item"]["ticket_id"]["S"]
        == ticket_put["Item"]["ticket_id"]["S"]
        == TICKET_ID
    )

    assert (
        operation_put["Item"]["operation_id"]["S"]
        == ticket_put["Item"]["operation_id"]["S"]
        == str(OPERATION_ID)
    )


def test_matching_existing_operation_replays_without_transaction() -> None:
    """FR-011/INV-007: matching durable retry returns original result."""

    client = FakeDynamoDBClient(
        get_item_responses=[stored_operation_item()],
    )
    service = coordinator(client)

    result = service.execute(
        operation(request_id=RETRY_REQUEST_ID)
    )

    assert result.status is TicketExecutionStatus.REPLAYED
    assert result.confirmation is not None
    assert result.confirmation.ticket_id == TICKET_ID
    assert result.request_id == RETRY_REQUEST_ID
    assert client.transaction_calls == []


def test_conflicting_existing_operation_is_rejected_without_write() -> None:
    """FR-012/INV-008: changed payload cannot reuse durable operation identity."""

    client = FakeDynamoDBClient(
        get_item_responses=[stored_operation_item()],
    )
    service = coordinator(client)

    result = service.execute(
        operation(
            request_id=RETRY_REQUEST_ID,
            environment="Firefox on Windows 11.",
        )
    )

    assert result.status is TicketExecutionStatus.CONFLICT
    assert result.confirmation is None
    assert client.transaction_calls == []


def test_concurrent_matching_race_reconciles_as_replay() -> None:
    """NFR-REL-001: losing a transaction race safely recovers original result."""

    client = FakeDynamoDBClient(
        get_item_responses=[
            {},
            stored_operation_item(),
        ],
        transaction_error=transaction_cancelled_error(),
    )
    service = coordinator(client)

    result = service.execute(operation())

    assert result.status is TicketExecutionStatus.REPLAYED
    assert result.confirmation is not None
    assert result.confirmation.ticket_id == TICKET_ID
    assert len(client.transaction_calls) == 1
    assert len(client.get_item_calls) == 2


def test_concurrent_conflicting_race_reconciles_as_conflict() -> None:
    """FR-012: losing to a different payload returns deterministic conflict."""

    client = FakeDynamoDBClient(
        get_item_responses=[
            {},
            stored_operation_item(
                environment="Firefox on Windows 11."
            ),
        ],
        transaction_error=transaction_cancelled_error(),
    )
    service = coordinator(client)

    result = service.execute(operation())

    assert result.status is TicketExecutionStatus.CONFLICT
    assert result.confirmation is None
    assert len(client.transaction_calls) == 1


def test_read_timeout_with_matching_durable_state_reconciles_as_replay() -> None:
    """NFR-REL-001/H-007: ambiguous timeout recovers authoritative state."""

    client = FakeDynamoDBClient(
        get_item_responses=[
            {},
            stored_operation_item(),
        ],
        transaction_error=read_timeout_error(),
    )
    service = coordinator(client)

    result = service.execute(operation())

    assert result.status is TicketExecutionStatus.REPLAYED
    assert result.confirmation is not None
    assert result.confirmation.ticket_id == TICKET_ID
    assert len(client.transaction_calls) == 1
    assert len(client.get_item_calls) == 2



def test_read_timeout_without_authoritative_state_is_unconfirmed() -> None:
    """H-007: ambiguous timeout without durable truth cannot claim success."""

    client = FakeDynamoDBClient(
        get_item_responses=[
            {},
            {},
        ],
        transaction_error=read_timeout_error(),
    )
    service = coordinator(client)

    result = service.execute(operation())

    assert result.status is TicketExecutionStatus.UNCONFIRMED
    assert result.confirmation is None
    assert len(client.transaction_calls) == 1
    assert len(client.get_item_calls) == 2


def test_cancelled_transaction_without_authoritative_state_is_unconfirmed() -> None:
    """H-007: ambiguous transaction outcome must never fabricate success."""

    client = FakeDynamoDBClient(
        get_item_responses=[
            {},
            {},
        ],
        transaction_error=transaction_cancelled_error(),
    )
    service = coordinator(client)

    result = service.execute(operation())

    assert result.status is TicketExecutionStatus.UNCONFIRMED
    assert result.confirmation is None


def test_access_denied_error_propagates_without_reconciliation() -> None:
    """H-007: non-ambiguous AWS service failures must not be rewritten."""

    client = FakeDynamoDBClient(
        get_item_responses=[{}],
        transaction_error=access_denied_error(),
    )
    service = coordinator(client)

    with pytest.raises(ClientError, match="Access denied."):
        service.execute(operation())

    assert len(client.transaction_calls) == 1
    assert len(client.get_item_calls) == 1


def test_access_denied_emits_authorization_failure_telemetry() -> None:
    """NFR-OBS-002/REL-004: access denial emits classified telemetry."""

    client = FakeDynamoDBClient(
        get_item_responses=[{}],
        transaction_error=access_denied_error(),
    )
    telemetry = RecordingFailureTelemetrySink()

    service = DynamoDBTicketExecutionCoordinator(
        dynamodb_client=client,
        operations_table_name=OPERATIONS_TABLE,
        tickets_table_name=TICKETS_TABLE,
        ticket_id_factory=lambda: TICKET_ID,
        clock=lambda: CONFIRMED_AT,
        failure_telemetry=telemetry,
    )

    with pytest.raises(ClientError, match="Access denied."):
        service.execute(operation())

    assert telemetry.events == [
        FailureEvent(
            occurred_at=CONFIRMED_AT,
            category=FailureCategory.AUTHORIZATION,
            request_id=FIRST_REQUEST_ID,
            operation_id=OPERATION_ID,
            error_code="AccessDeniedException",
        )
    ]


def test_telemetry_failure_does_not_mask_access_denied_error() -> None:
    """FM-011: telemetry failure must not replace the business failure."""

    client = FakeDynamoDBClient(
        get_item_responses=[{}],
        transaction_error=access_denied_error(),
    )
    telemetry = FailingFailureTelemetrySink()

    service = DynamoDBTicketExecutionCoordinator(
        dynamodb_client=client,
        operations_table_name=OPERATIONS_TABLE,
        tickets_table_name=TICKETS_TABLE,
        ticket_id_factory=lambda: TICKET_ID,
        clock=lambda: CONFIRMED_AT,
        failure_telemetry=telemetry,
    )

    with pytest.raises(ClientError, match="Access denied."):
        service.execute(operation())


def test_incomplete_matching_state_is_unconfirmed() -> None:
    """H-007: incomplete durable state cannot be treated as confirmation."""

    fingerprint = bug_report_fingerprint(complete_bug_report())

    client = FakeDynamoDBClient(
        get_item_responses=[
            {
                "Item": {
                    "operation_id": {
                        "S": str(OPERATION_ID),
                    },
                    "payload_fingerprint": {
                        "S": fingerprint,
                    },
                }
            }
        ],
    )
    service = coordinator(client)

    result = service.execute(operation())

    assert result.status is TicketExecutionStatus.UNCONFIRMED
    assert result.confirmation is None
    assert client.transaction_calls == []