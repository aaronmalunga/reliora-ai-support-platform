"""Canonical operational failure telemetry contracts for Reliora."""

from enum import StrEnum
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict


class FailureCategory(StrEnum):
    """Classify operational failures using Reliora's documented taxonomy."""

    VALIDATION = "VALIDATION"
    ROUTING = "ROUTING"
    KNOWLEDGE = "KNOWLEDGE"
    AUTHORIZATION = "AUTHORIZATION"
    MODEL = "MODEL"
    TOOL = "TOOL"
    BACKEND = "BACKEND"
    PERSISTENCE = "PERSISTENCE"
    IDEMPOTENCY = "IDEMPOTENCY"
    TIMEOUT = "TIMEOUT"
    THROTTLING = "THROTTLING"
    SECURITY = "SECURITY"
    TELEMETRY = "TELEMETRY"
    DEPLOYMENT = "DEPLOYMENT"
    UNKNOWN = "UNKNOWN"


class FailureEvent(BaseModel):
    """Represent one structured operational failure without customer payloads."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    occurred_at: AwareDatetime
    category: FailureCategory
    request_id: UUID | None = None
    session_id: UUID | None = None
    operation_id: UUID | None = None
    error_code: str | None = None
