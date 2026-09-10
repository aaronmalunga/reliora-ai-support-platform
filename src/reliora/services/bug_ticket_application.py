"""Application service for safe bug-ticket submission."""

from pydantic import BaseModel, ConfigDict

from reliora.domain.operations import BugReportOperation
from reliora.policy.authorization import (
    AuthorizationPreconditionDecision,
    AuthorizationPreconditionStatus,
    evaluate_bug_report_preconditions,
)
from reliora.services.ticket_execution import (
    TicketExecutionPort,
    TicketExecutionResult,
)


class BugTicketApplicationResult(BaseModel):
    """Combined authorization and execution outcome for one ticket request."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    authorization: AuthorizationPreconditionDecision
    execution: TicketExecutionResult | None = None


class BugTicketApplicationService:
    """Enforce authorization before ticket side-effect coordination."""

    def __init__(
        self,
        *,
        ticket_execution: TicketExecutionPort,
    ) -> None:
        self._ticket_execution = ticket_execution

    def submit(
        self,
        operation: BugReportOperation,
    ) -> BugTicketApplicationResult:
        """Authorize a logical ticket operation before execution."""

        authorization = evaluate_bug_report_preconditions(operation)

        if authorization.status is AuthorizationPreconditionStatus.DENIED:
            return BugTicketApplicationResult(
                authorization=authorization,
            )

        execution = self._ticket_execution.execute(operation)

        return BugTicketApplicationResult(
            authorization=authorization,
            execution=execution,
        )