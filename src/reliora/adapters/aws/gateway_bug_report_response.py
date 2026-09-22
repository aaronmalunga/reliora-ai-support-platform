"""Translate Reliora ticket outcomes into AgentCore Gateway tool responses."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from reliora.policy.authorization import AuthorizationPreconditionStatus
from reliora.services.bug_ticket_application import BugTicketApplicationResult
from reliora.services.ticket_execution import TicketExecutionStatus


class GatewayBugReportResponse(BaseModel):
    """External response contract for the create_bug_report Gateway tool."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    status: Literal[
        "OPEN",
        "REJECTED",
        "CONFLICT",
        "UNCONFIRMED",
    ]
    ticket_id: str | None = Field(
        default=None,
        serialization_alias="ticketId",
    )
    execution_status: TicketExecutionStatus | None = Field(
        default=None,
        serialization_alias="executionStatus",
    )
    error_code: str | None = Field(
        default=None,
        serialization_alias="errorCode",
    )
    missing_fields: tuple[str, ...] = Field(
        default=(),
        serialization_alias="missingFields",
    )


def serialize_bug_ticket_result(
    result: BugTicketApplicationResult,
) -> dict[str, object]:
    """Return a safe model-facing response for one ticket operation."""

    if (
        result.authorization.status
        is AuthorizationPreconditionStatus.DENIED
    ):
        response = GatewayBugReportResponse(
            status="REJECTED",
            error_code=result.authorization.reason.value,
            missing_fields=tuple(
                field.value
                for field in result.authorization.missing_fields
            ),
        )

        return response.model_dump(
            by_alias=True,
            mode="json",
            exclude_none=True,
            exclude_defaults=True,
        )

    execution = result.execution

    if execution is None:
        raise ValueError(
            "Authorized ticket result is missing an execution outcome."
        )

    if execution.status in {
        TicketExecutionStatus.CREATED,
        TicketExecutionStatus.REPLAYED,
    }:
        confirmation = execution.confirmation

        if confirmation is None:
            raise ValueError(
                "Successful ticket execution is missing confirmation."
            )

        response = GatewayBugReportResponse(
            status="OPEN",
            ticket_id=confirmation.ticket_id,
            execution_status=execution.status,
        )

        return response.model_dump(
            by_alias=True,
            mode="json",
            exclude_none=True,
            exclude_defaults=True,
        )

    if execution.status is TicketExecutionStatus.CONFLICT:
        response = GatewayBugReportResponse(
            status="CONFLICT",
            execution_status=execution.status,
            error_code="IDEMPOTENCY_CONFLICT",
        )

        return response.model_dump(
            by_alias=True,
            mode="json",
            exclude_none=True,
            exclude_defaults=True,
        )

    response = GatewayBugReportResponse(
        status="UNCONFIRMED",
        execution_status=execution.status,
        error_code="TICKET_OUTCOME_UNCONFIRMED",
    )

    return response.model_dump(
        by_alias=True,
        mode="json",
        exclude_none=True,
        exclude_defaults=True,
    )