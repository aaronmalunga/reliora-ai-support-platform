"""Domain contracts for Reliora side-effecting operations."""

from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from reliora.domain.bug import BugReportDraft


class BugReportOperation(BaseModel):
    """One logical proposal to create a bug-report ticket."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    operation_id: UUID = Field(default_factory=uuid4)
    request_id: UUID
    session_id: UUID
    bug_report: BugReportDraft