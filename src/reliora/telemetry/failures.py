"""Canonical operational failure categories for Reliora telemetry."""

from enum import StrEnum


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
