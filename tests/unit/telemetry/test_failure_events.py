from datetime import UTC, datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from reliora.telemetry.failures import FailureCategory, FailureEvent

REQUEST_ID = UUID("11111111-1111-4111-8111-111111111111")
SESSION_ID = UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")
OPERATION_ID = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
OCCURRED_AT = datetime(2026, 9, 10, 18, 30, tzinfo=UTC)


def test_failure_event_serializes_safe_correlation_context() -> None:
    """NFR-OBS-001/002: failure telemetry is structured and correlatable."""

    event = FailureEvent(
        occurred_at=OCCURRED_AT,
        category=FailureCategory.PERSISTENCE,
        request_id=REQUEST_ID,
        session_id=SESSION_ID,
        operation_id=OPERATION_ID,
        error_code="DYNAMODB_READ_TIMEOUT",
    )

    assert event.model_dump(mode="json", exclude_none=True) == {
        "occurred_at": "2026-09-10T18:30:00Z",
        "category": "PERSISTENCE",
        "request_id": str(REQUEST_ID),
        "session_id": str(SESSION_ID),
        "operation_id": str(OPERATION_ID),
        "error_code": "DYNAMODB_READ_TIMEOUT",
    }


def test_failure_event_rejects_unstructured_customer_payload() -> None:
    """NFR-PRIV-002: arbitrary customer payloads are not telemetry fields."""

    with pytest.raises(ValidationError):
        FailureEvent(
            occurred_at=OCCURRED_AT,
            category=FailureCategory.VALIDATION,
            request_id=REQUEST_ID,
            customer_payload="raw customer content",
        )
