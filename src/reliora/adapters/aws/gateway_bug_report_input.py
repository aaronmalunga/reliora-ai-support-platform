"""Translate AgentCore Gateway bug-report tool input into Reliora domain state."""

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from reliora.domain.bug import BugReportDraft


class GatewayBugReportInput(BaseModel):
    """Model-facing input contract for the create_bug_report Gateway tool."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    description: str
    steps_to_reproduce: str = Field(alias="stepsToReproduce")
    environment: str


def parse_gateway_bug_report(
    event: Mapping[str, Any],
) -> BugReportDraft:
    """Translate one Gateway tool invocation into validated domain state."""

    gateway_input = GatewayBugReportInput.model_validate(dict(event))

    return BugReportDraft(
        description=gateway_input.description,
        steps_to_reproduce=gateway_input.steps_to_reproduce,
        environment=gateway_input.environment,
    )