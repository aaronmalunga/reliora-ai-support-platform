"""Domain contracts for authoritative ticket outcomes."""

from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class TicketCreationConfirmation(BaseModel):
    """Authoritative backend confirmation that a ticket was created."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    operation_id: UUID
    ticket_id: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    confirmed_at: AwareDatetime