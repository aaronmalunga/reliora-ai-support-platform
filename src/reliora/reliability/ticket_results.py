"""Reference storage for authoritative ticket-operation results."""

from uuid import UUID

from reliora.domain.tickets import TicketCreationConfirmation


class InMemoryTicketResultStore:
    """Local reference store for confirmed ticket-operation results."""

    def __init__(self) -> None:
        self._confirmations: dict[UUID, TicketCreationConfirmation] = {}

    def get(
        self,
        operation_id: UUID,
    ) -> TicketCreationConfirmation | None:
        """Return the stored authoritative result for an operation, if present."""

        return self._confirmations.get(operation_id)

    def save(
        self,
        confirmation: TicketCreationConfirmation,
    ) -> TicketCreationConfirmation:
        """Persist an authoritative result without allowing silent replacement."""

        existing = self._confirmations.get(confirmation.operation_id)

        if existing is None:
            self._confirmations[confirmation.operation_id] = confirmation
            return confirmation

        if existing == confirmation:
            return existing

        raise ValueError(
            "A different ticket confirmation already exists for operation_id "
            f"{confirmation.operation_id}."
        )