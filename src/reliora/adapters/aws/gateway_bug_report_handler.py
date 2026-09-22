"""Compose the Reliora bug-ticket workflow for AgentCore Gateway."""

from collections.abc import Mapping
from typing import Any

from reliora.adapters.aws.gateway_bug_report_operation import (
    TrustedOperationIdentity,
    build_gateway_bug_report_operation,
)
from reliora.adapters.aws.gateway_bug_report_response import (
    serialize_bug_ticket_result,
)
from reliora.services.bug_ticket_application import (
    BugTicketApplicationService,
)
from reliora.services.ticket_execution import TicketExecutionPort


class GatewayBugReportHandler:
    """Run one Gateway bug-report invocation through Reliora."""

    def __init__(
        self,
        *,
        ticket_execution: TicketExecutionPort,
    ) -> None:
        self._application = BugTicketApplicationService(
            ticket_execution=ticket_execution,
        )

    def handle(
        self,
        event: Mapping[str, Any],
        *,
        identity: TrustedOperationIdentity,
    ) -> dict[str, object]:
        """Process one validated and trusted Gateway ticket invocation."""

        operation = build_gateway_bug_report_operation(
            event,
            identity=identity,
        )

        result = self._application.submit(operation)

        return serialize_bug_ticket_result(result)