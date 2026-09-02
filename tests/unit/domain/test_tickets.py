"""Unit tests for authoritative ticket-result contracts."""

from datetime import UTC, datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from reliora.domain.tickets import TicketCreationConfirmation


def valid_confirmation() -> TicketCreationConfirmation:
    """Return a valid authoritative ticket confirmation."""

    return TicketCreationConfirmation(
        operation_id=UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
        ticket_id="BUG-12345",
        provider="reference-ticket-provider",
        confirmed_at=datetime(
            2026,
            9,
            2,
            16,
            0,
            tzinfo=UTC,
        ),
    )


def test_valid_ticket_confirmation_is_accepted() -> None:
    """FR-013: authoritative backend confirmation has a typed contract."""

    confirmation = valid_confirmation()

    assert confirmation.ticket_id == "BUG-12345"
    assert confirmation.provider == "reference-ticket-provider"


def test_confirmation_is_bound_to_operation_id() -> None:
    """FR-003/FR-013: confirmation identifies its logical operation."""

    confirmation = valid_confirmation()

    assert confirmation.operation_id == UUID(
        "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
    )


@pytest.mark.parametrize("field_name", ["ticket_id", "provider"])
def test_required_text_fields_reject_blank_values(field_name: str) -> None:
    """INV-009/INV-010: empty backend-confirmation fields are invalid."""

    raw_confirmation = {
        "operation_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
        "ticket_id": "BUG-12345",
        "provider": "reference-ticket-provider",
        "confirmed_at": "2026-09-02T16:00:00+00:00",
    }
    raw_confirmation[field_name] = "   "

    with pytest.raises(ValidationError):
        TicketCreationConfirmation.model_validate(raw_confirmation)


def test_confirmation_requires_timezone_aware_timestamp() -> None:
    """NFR-OBS-003: confirmation timestamps must be unambiguous."""

    with pytest.raises(ValidationError):
        TicketCreationConfirmation(
            operation_id=UUID(
                "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
            ),
            ticket_id="BUG-12345",
            provider="reference-ticket-provider",
            confirmed_at=datetime(2026, 9, 2, 16, 0, tzinfo=UTC).replace(
                tzinfo=None
            ),
        )
def test_confirmation_rejects_unexpected_success_flag() -> None:
    """FR-013: callers cannot inject an arbitrary success flag."""

    raw_confirmation = {
        "operation_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
        "ticket_id": "BUG-12345",
        "provider": "reference-ticket-provider",
        "confirmed_at": "2026-09-02T16:00:00+00:00",
        "success": True,
    }

    with pytest.raises(ValidationError):
        TicketCreationConfirmation.model_validate(raw_confirmation)


def test_confirmation_is_immutable() -> None:
    """Authoritative backend evidence cannot be silently mutated."""

    confirmation = valid_confirmation()

    with pytest.raises(ValidationError):
        confirmation.ticket_id = "BUG-99999"