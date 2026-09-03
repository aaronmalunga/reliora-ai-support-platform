"""Construct trusted Reliora operations from AgentCore Gateway input."""

from collections.abc import Mapping
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from reliora.adapters.aws.gateway_bug_report_input import (
    parse_gateway_bug_report,
)
from reliora.domain.operations import BugReportOperation


class TrustedOperationIdentity(BaseModel):
    """Identifiers supplied by a trusted application or transport boundary."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    operation_id: UUID
    request_id: UUID
    session_id: UUID


def build_gateway_bug_report_operation(
    event: Mapping[str, Any],
    *,
    identity: TrustedOperationIdentity,
) -> BugReportOperation:
    """Create one logical bug-ticket operation from trusted and untrusted input."""

    bug_report = parse_gateway_bug_report(event)

    return BugReportOperation(
        operation_id=identity.operation_id,
        request_id=identity.request_id,
        session_id=identity.session_id,
        bug_report=bug_report,
    )