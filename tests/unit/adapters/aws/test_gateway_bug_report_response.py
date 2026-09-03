"""Tests for AgentCore Gateway bug-report response translation."""

from datetime import UTC, datetime
from uuid import UUID

import pytest

from reliora.adapters.aws.gateway_bug_report_response import (
    serialize_bug_ticket_result,
)
from reliora.domain.bug import BugField
from reliora.domain.tickets import TicketCreationConfirmation
from reliora.policy.authorization import (
    AuthorizationPreconditionDecision,
    AuthorizationPreconditionStatus,
    AuthorizationReason,
)
from reliora.services.bug_ticket_application import (
    BugTicketApplicationResult,
)
from reliora.services.ticket_execution import (
    TicketExecutionResult,
    TicketExecutionStatus,
)

OPERATION_ID = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
REQUEST_ID = UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")
CONFIRMED_AT = datetime(2026, 9, 3, 20, 0, tzinfo=UTC)


def _authorized() -> AuthorizationPreconditionDecision:
    return AuthorizationPreconditionDecision(
        operation_id=OPERATION_ID,
        request_id=REQUEST_ID,
        status=(
            AuthorizationPreconditionStatus.READY_FOR_IDEMPOTENCY_CHECK
        ),
        reason=AuthorizationReason.PRECONDITIONS_SATISFIED,
    )


def _confirmation() -> TicketCreationConfirmation:
    return TicketCreationConfirmation(
        operation_id=OPERATION_ID,
        ticket_id="BUG-123",
        provider="reliora-dynamodb",
        confirmed_at=CONFIRMED_AT,
    )


def test_created_ticket_preserves_course_success_contract() -> None:
    result = BugTicketApplicationResult(
        authorization=_authorized(),
        execution=TicketExecutionResult(
            operation_id=OPERATION_ID,
            request_id=REQUEST_ID,
            status=TicketExecutionStatus.CREATED,
            confirmation=_confirmation(),
        ),
    )

    response = serialize_bug_ticket_result(result)

    assert response == {
        "status": "OPEN",
        "ticketId": "BUG-123",
        "executionStatus": "CREATED",
    }


def test_replayed_ticket_returns_same_authoritative_ticket() -> None:
    result = BugTicketApplicationResult(
        authorization=_authorized(),
        execution=TicketExecutionResult(
            operation_id=OPERATION_ID,
            request_id=REQUEST_ID,
            status=TicketExecutionStatus.REPLAYED,
            confirmation=_confirmation(),
        ),
    )

    response = serialize_bug_ticket_result(result)

    assert response == {
        "status": "OPEN",
        "ticketId": "BUG-123",
        "executionStatus": "REPLAYED",
    }


def test_conflict_does_not_claim_ticket_creation() -> None:
    result = BugTicketApplicationResult(
        authorization=_authorized(),
        execution=TicketExecutionResult(
            operation_id=OPERATION_ID,
            request_id=REQUEST_ID,
            status=TicketExecutionStatus.CONFLICT,
        ),
    )

    response = serialize_bug_ticket_result(result)

    assert response == {
        "status": "CONFLICT",
        "executionStatus": "CONFLICT",
        "errorCode": "IDEMPOTENCY_CONFLICT",
    }
    assert "ticketId" not in response


def test_unconfirmed_outcome_does_not_claim_ticket_creation() -> None:
    result = BugTicketApplicationResult(
        authorization=_authorized(),
        execution=TicketExecutionResult(
            operation_id=OPERATION_ID,
            request_id=REQUEST_ID,
            status=TicketExecutionStatus.UNCONFIRMED,
        ),
    )

    response = serialize_bug_ticket_result(result)

    assert response == {
        "status": "UNCONFIRMED",
        "executionStatus": "UNCONFIRMED",
        "errorCode": "TICKET_OUTCOME_UNCONFIRMED",
    }
    assert "ticketId" not in response


def test_denied_request_returns_missing_fields() -> None:
    result = BugTicketApplicationResult(
        authorization=AuthorizationPreconditionDecision(
            operation_id=OPERATION_ID,
            request_id=REQUEST_ID,
            status=AuthorizationPreconditionStatus.DENIED,
            reason=AuthorizationReason.INCOMPLETE_BUG_REPORT,
            missing_fields=(BugField.ENVIRONMENT,),
        ),
    )

    response = serialize_bug_ticket_result(result)

    assert response == {
        "status": "REJECTED",
        "errorCode": "INCOMPLETE_BUG_REPORT",
        "missingFields": ["environment"],
    }


def test_authorized_result_requires_execution_outcome() -> None:
    result = BugTicketApplicationResult(
        authorization=_authorized(),
    )

    with pytest.raises(
        ValueError,
        match="missing an execution outcome",
    ):
        serialize_bug_ticket_result(result)


def test_successful_execution_requires_backend_confirmation() -> None:
    result = BugTicketApplicationResult(
        authorization=_authorized(),
        execution=TicketExecutionResult(
            operation_id=OPERATION_ID,
            request_id=REQUEST_ID,
            status=TicketExecutionStatus.CREATED,
        ),
    )

    with pytest.raises(
        ValueError,
        match="missing confirmation",
    ):
        serialize_bug_ticket_result(result)