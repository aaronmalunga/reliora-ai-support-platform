"""DynamoDB-backed execution for durable bug-ticket side effects."""

from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from typing import Any, Protocol
from uuid import UUID, uuid4

from botocore.exceptions import ClientError
from pydantic import ValidationError

from reliora.domain.operations import BugReportOperation
from reliora.domain.tickets import TicketCreationConfirmation
from reliora.reliability.idempotency import bug_report_fingerprint
from reliora.services.ticket_execution import (
    TicketExecutionResult,
    TicketExecutionStatus,
)


class DynamoDBClient(Protocol):
    """Minimal DynamoDB API required by the durable execution adapter."""

    def get_item(self, **kwargs: Any) -> dict[str, Any]:
        """Return one DynamoDB item."""
        ...

    def transact_write_items(self, **kwargs: Any) -> dict[str, Any]:
        """Atomically write multiple DynamoDB items."""
        ...


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC timestamp."""

    return datetime.now(UTC)


def _ticket_id() -> str:
    """Return a collision-resistant Reliora reference ticket identifier."""

    return f"BUG-{uuid4()}"


def _string_attribute(
    item: Mapping[str, Any],
    name: str,
) -> str | None:
    """Return one DynamoDB string attribute when it is well formed."""

    attribute = item.get(name)

    if not isinstance(attribute, Mapping):
        return None

    value = attribute.get("S")

    if not isinstance(value, str) or not value:
        return None

    return value


class DynamoDBTicketExecutionCoordinator:
    """Execute ticket operations with durable DynamoDB idempotency."""

    def __init__(
        self,
        *,
        dynamodb_client: DynamoDBClient,
        operations_table_name: str,
        tickets_table_name: str,
        provider_name: str = "reliora-dynamodb",
        ticket_id_factory: Callable[[], str] = _ticket_id,
        clock: Callable[[], datetime] = _utc_now,
    ) -> None:
        self._dynamodb = dynamodb_client
        self._operations_table_name = operations_table_name
        self._tickets_table_name = tickets_table_name
        self._provider_name = provider_name
        self._ticket_id_factory = ticket_id_factory
        self._clock = clock

    def execute(
        self,
        operation: BugReportOperation,
    ) -> TicketExecutionResult:
        """Create, replay, or reject one durable logical ticket operation."""

        fingerprint = bug_report_fingerprint(operation.bug_report)

        existing_item = self._load_operation(operation.operation_id)

        if existing_item is not None:
            return self._result_from_existing(
                operation=operation,
                expected_fingerprint=fingerprint,
                item=existing_item,
            )

        confirmed_at = self._clock()
        confirmation = TicketCreationConfirmation(
            operation_id=operation.operation_id,
            ticket_id=self._ticket_id_factory(),
            provider=self._provider_name,
            confirmed_at=confirmed_at,
        )

        try:
            self._create_operation_and_ticket(
                operation=operation,
                fingerprint=fingerprint,
                confirmation=confirmation,
            )
        except ClientError as error:
            error_code = error.response.get("Error", {}).get("Code")

            if error_code != "TransactionCanceledException":
                raise

            reconciled_item = self._load_operation(operation.operation_id)

            if reconciled_item is None:
                return TicketExecutionResult(
                    operation_id=operation.operation_id,
                    request_id=operation.request_id,
                    status=TicketExecutionStatus.UNCONFIRMED,
                )

            return self._result_from_existing(
                operation=operation,
                expected_fingerprint=fingerprint,
                item=reconciled_item,
            )

        return TicketExecutionResult(
            operation_id=operation.operation_id,
            request_id=operation.request_id,
            status=TicketExecutionStatus.CREATED,
            confirmation=confirmation,
        )

    def _load_operation(
        self,
        operation_id: UUID,
    ) -> Mapping[str, Any] | None:
        """Load durable operation state using a strongly consistent read."""

        response = self._dynamodb.get_item(
            TableName=self._operations_table_name,
            Key={
                "operation_id": {
                    "S": str(operation_id),
                }
            },
            ConsistentRead=True,
        )

        item = response.get("Item")

        if not isinstance(item, Mapping):
            return None

        return item

    def _result_from_existing(
        self,
        *,
        operation: BugReportOperation,
        expected_fingerprint: str,
        item: Mapping[str, Any],
    ) -> TicketExecutionResult:
        """Classify existing durable state as replay, conflict, or unknown."""

        stored_fingerprint = _string_attribute(
            item,
            "payload_fingerprint",
        )

        if stored_fingerprint is None:
            return self._unconfirmed(operation)

        if stored_fingerprint != expected_fingerprint:
            return TicketExecutionResult(
                operation_id=operation.operation_id,
                request_id=operation.request_id,
                status=TicketExecutionStatus.CONFLICT,
            )

        ticket_id = _string_attribute(item, "ticket_id")
        provider = _string_attribute(item, "provider")
        confirmed_at = _string_attribute(item, "confirmed_at")

        if ticket_id is None or provider is None or confirmed_at is None:
            return self._unconfirmed(operation)

        try:
            confirmation = TicketCreationConfirmation.model_validate(
                {
                    "operation_id": operation.operation_id,
                    "ticket_id": ticket_id,
                    "provider": provider,
                    "confirmed_at": confirmed_at,
                }
            )
        except ValidationError:
            return self._unconfirmed(operation)

        return TicketExecutionResult(
            operation_id=operation.operation_id,
            request_id=operation.request_id,
            status=TicketExecutionStatus.REPLAYED,
            confirmation=confirmation,
        )

    def _create_operation_and_ticket(
        self,
        *,
        operation: BugReportOperation,
        fingerprint: str,
        confirmation: TicketCreationConfirmation,
    ) -> None:
        """Atomically create durable operation and ticket records."""

        confirmed_at = confirmation.confirmed_at.isoformat()

        self._dynamodb.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": self._operations_table_name,
                        "Item": {
                            "operation_id": {
                                "S": str(operation.operation_id),
                            },
                            "payload_fingerprint": {
                                "S": fingerprint,
                            },
                            "ticket_id": {
                                "S": confirmation.ticket_id,
                            },
                            "provider": {
                                "S": confirmation.provider,
                            },
                            "confirmed_at": {
                                "S": confirmed_at,
                            },
                        },
                        "ConditionExpression": (
                            "attribute_not_exists(operation_id)"
                        ),
                    }
                },
                {
                    "Put": {
                        "TableName": self._tickets_table_name,
                        "Item": {
                            "ticket_id": {
                                "S": confirmation.ticket_id,
                            },
                            "operation_id": {
                                "S": str(operation.operation_id),
                            },
                            "description": {
                                "S": operation.bug_report.description or "",
                            },
                            "steps_to_reproduce": {
                                "S": (
                                    operation.bug_report.steps_to_reproduce
                                    or ""
                                ),
                            },
                            "environment": {
                                "S": operation.bug_report.environment or "",
                            },
                            "created_at": {
                                "S": confirmed_at,
                            },
                        },
                        "ConditionExpression": (
                            "attribute_not_exists(ticket_id)"
                        ),
                    }
                },
            ]
        )

    @staticmethod
    def _unconfirmed(
        operation: BugReportOperation,
    ) -> TicketExecutionResult:
        """Return an explicit ambiguous-state result without guessing."""

        return TicketExecutionResult(
            operation_id=operation.operation_id,
            request_id=operation.request_id,
            status=TicketExecutionStatus.UNCONFIRMED,
        )