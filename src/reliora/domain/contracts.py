"""Core typed contracts for the Reliora runtime."""

from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Intent(StrEnum):
    """Top-level customer-support intent defined by FR-004."""

    BUG = "BUG"
    PLATFORM = "PLATFORM"
    OTHER = "OTHER"


class SupportRequest(BaseModel):
    """Validated customer request accepted by the Reliora runtime."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    request_id: UUID = Field(default_factory=uuid4)
    session_id: UUID = Field(default_factory=uuid4)
    message: str = Field(min_length=1)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        """Reject requests that contain no meaningful customer text."""

        normalized = value.strip()

        if not normalized:
            raise ValueError("message must contain non-whitespace text")

        return normalized


class RoutingDecision(BaseModel):
    """Machine-verifiable top-level routing result for one request."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    request_id: UUID
    intent: Intent
    routing_version: str = Field(min_length=1)

    @field_validator("routing_version")
    @classmethod
    def validate_routing_version(cls, value: str) -> str:
        """Require a non-empty routing provenance identifier."""

        normalized = value.strip()

        if not normalized:
            raise ValueError("routing_version must contain non-whitespace text")

        return normalized