"""Lambda-style runtime composition for the Reliora bug-ticket workflow."""

from collections.abc import Mapping
from typing import Any

from reliora.adapters.aws.gateway_bug_report_handler import (
    GatewayBugReportHandler,
)
from reliora.adapters.aws.operation_identity_resolver import (
    OperationIdentityResolver,
)
from reliora.services.ticket_execution import TicketExecutionPort


class LambdaBugReportRuntime:
    """Adapt Lambda event/context inputs to the Reliora Gateway workflow."""

    def __init__(
        self,
        *,
        ticket_execution: TicketExecutionPort,
        identity_resolver: OperationIdentityResolver,
    ) -> None:
        self._handler = GatewayBugReportHandler(
            ticket_execution=ticket_execution,
        )
        self._identity_resolver = identity_resolver

    def handle(
        self,
        event: Mapping[str, Any],
        context: object,
    ) -> dict[str, object]:
        """Handle one Lambda-style Gateway invocation."""

        identity = self._identity_resolver.resolve(context)

        return self._handler.handle(
            event,
            identity=identity,
        )