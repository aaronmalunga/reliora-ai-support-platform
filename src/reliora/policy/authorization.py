"""Deterministic authorization preconditions for Reliora operations."""

from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from reliora.domain.bug import BugField
from reliora.domain.operations import BugReportOperation


class AuthorizationPreconditionStatus(StrEnum):
    """Outcome of deterministic checks before idempotency authorization."""

    DENIED = "DENIED"
    READY_FOR_IDEMPOTENCY_CHECK = "READY_FOR_IDEMPOTENCY_CHECK"


class AuthorizationReason(StrEnum):
    """Machine-readable reason for a pre-authorization decision."""

    INCOMPLETE_BUG_REPORT = "INCOMPLETE_BUG_REPORT"
    PRECONDITIONS_SATISFIED = "PRECONDITIONS_SATISFIED"


class AuthorizationPreconditionDecision(BaseModel):
    """Deterministic decision produced before the idempotency boundary."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    operation_id: UUID
    request_id: UUID
    status: AuthorizationPreconditionStatus
    reason: AuthorizationReason
    missing_fields: tuple[BugField, ...] = ()


def evaluate_bug_report_preconditions(
    operation: BugReportOperation,
) -> AuthorizationPreconditionDecision:
    """Evaluate deterministic prerequisites for a bug-ticket operation."""

    missing_fields = operation.bug_report.missing_fields

    if missing_fields:
        return AuthorizationPreconditionDecision(
            operation_id=operation.operation_id,
            request_id=operation.request_id,
            status=AuthorizationPreconditionStatus.DENIED,
            reason=AuthorizationReason.INCOMPLETE_BUG_REPORT,
            missing_fields=missing_fields,
        )

    return AuthorizationPreconditionDecision(
        operation_id=operation.operation_id,
        request_id=operation.request_id,
        status=AuthorizationPreconditionStatus.READY_FOR_IDEMPOTENCY_CHECK,
        reason=AuthorizationReason.PRECONDITIONS_SATISFIED,
    )