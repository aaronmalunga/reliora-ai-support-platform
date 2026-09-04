"""Resolve trusted execution identity at the AWS runtime boundary."""

from typing import Protocol

from reliora.adapters.aws.gateway_bug_report_operation import (
    TrustedOperationIdentity,
)


class OperationIdentityResolver(Protocol):
    """Resolve trusted Reliora identifiers from runtime-owned context."""

    def resolve(
        self,
        context: object,
    ) -> TrustedOperationIdentity:
        """Return identity for one logical Gateway ticket invocation."""
        ...