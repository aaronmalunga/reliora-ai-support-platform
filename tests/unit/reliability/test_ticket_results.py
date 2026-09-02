"""Unit tests for authoritative ticket-result storage."""

from datetime import UTC, datetime
from uuid import UUID

import pytest

from reliora.domain.tickets import TicketCreationConfirmation
from reliora.reliability.ticket_results import InMemoryTicketResultStore

OPERATION_ID = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")


def confirmation(
    *,
    ticket_id: str = "BUG-12345",
) -> TicketCreationConfirmation:
    """Return an authoritative confirmation for the reference operation."""

    return TicketCreationConfirmation(
        operation_id=OPERATION_ID,
        ticket_id=ticket_id,
        provider="reference-ticket-provider",
        confirmed_at=datetime(2026, 9, 2, 16, 0, tzinfo=UTC),
    )


def test_unknown_operation_has_no_confirmed_result() -> None:
    """FR-013/H-007: absence of backend confirmation remains explicit."""

    store = InMemoryTicketResultStore()

    assert store.get(OPERATION_ID) is None


def test_confirmation_can_be_saved_and_retrieved() -> None:
    """FR-011: an authoritative result can be recovered for retry replay."""

    store = InMemoryTicketResultStore()
    expected = confirmation()

    saved = store.save(expected)

    assert saved == expected
    assert store.get(OPERATION_ID) == expected


def test_saving_identical_confirmation_is_idempotent() -> None:
    """NFR-REL-001: repeating the same confirmed write is safe."""

    store = InMemoryTicketResultStore()
    expected = confirmation()

    first = store.save(expected)
    second = store.save(expected)

    assert first == second
    assert store.get(OPERATION_ID) == expected


def test_different_confirmation_cannot_replace_existing_result() -> None:
    """INV-007/INV-010: confirmed operation identity cannot be remapped."""

    store = InMemoryTicketResultStore()
    original = confirmation(ticket_id="BUG-12345")
    conflicting = confirmation(ticket_id="BUG-99999")

    store.save(original)

    with pytest.raises(
        ValueError,
        match="different ticket confirmation already exists",
    ):
        store.save(conflicting)

    assert store.get(OPERATION_ID) == original


def test_different_operations_store_independent_results() -> None:
    """FR-003: separate logical operations retain separate backend results."""

    store = InMemoryTicketResultStore()

    first = confirmation()

    second_operation_id = UUID(
        "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
    )
    second = TicketCreationConfirmation(
        operation_id=second_operation_id,
        ticket_id="BUG-67890",
        provider="reference-ticket-provider",
        confirmed_at=datetime(2026, 9, 2, 16, 5, tzinfo=UTC),
    )

    store.save(first)
    store.save(second)

    assert store.get(OPERATION_ID) == first
    assert store.get(second_operation_id) == second