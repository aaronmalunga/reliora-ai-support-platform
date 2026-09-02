"""Provider contract for authoritative bug-ticket creation."""

from typing import Protocol

from reliora.domain.operations import BugReportOperation
from reliora.domain.tickets import TicketCreationConfirmation


class TicketProvider(Protocol):
    """Port for an authoritative bug-ticket backend."""

    def create_bug_ticket(
        self,
        operation: BugReportOperation,
    ) -> TicketCreationConfirmation:
        """Create one bug ticket and return authoritative confirmation."""
        ...