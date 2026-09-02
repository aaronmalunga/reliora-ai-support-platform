"""Reference idempotency controls for Reliora side-effecting operations."""

import hashlib
import json
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from reliora.domain.bug import BugReportDraft
from reliora.domain.operations import BugReportOperation


class IdempotencyStatus(StrEnum):
    """Outcome of comparing a logical operation with prior operation state."""

    NEW_OPERATION = "NEW_OPERATION"
    MATCHING_OPERATION = "MATCHING_OPERATION"
    CONFLICT = "CONFLICT"


class IdempotencyDecision(BaseModel):
    """Machine-verifiable result of an idempotency admission check."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    operation_id: UUID
    request_id: UUID
    status: IdempotencyStatus
    payload_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")


def bug_report_fingerprint(bug_report: BugReportDraft) -> str:
    """Create a deterministic fingerprint of normalized bug-report data."""

    canonical_payload = json.dumps(
        bug_report.model_dump(mode="json"),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    return hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()


class InMemoryIdempotencyRegistry:
    """Local reference registry for deterministic idempotency behaviour."""

    def __init__(self) -> None:
        self._fingerprints: dict[UUID, str] = {}

    def check_and_register(
        self,
        operation: BugReportOperation,
    ) -> IdempotencyDecision:
        """Classify an operation as new, matching, or conflicting."""

        fingerprint = bug_report_fingerprint(operation.bug_report)
        existing_fingerprint = self._fingerprints.get(operation.operation_id)

        if existing_fingerprint is None:
            self._fingerprints[operation.operation_id] = fingerprint

            status = IdempotencyStatus.NEW_OPERATION

        elif existing_fingerprint == fingerprint:
            status = IdempotencyStatus.MATCHING_OPERATION

        else:
            status = IdempotencyStatus.CONFLICT

        return IdempotencyDecision(
            operation_id=operation.operation_id,
            request_id=operation.request_id,
            status=status,
            payload_fingerprint=fingerprint,
        )