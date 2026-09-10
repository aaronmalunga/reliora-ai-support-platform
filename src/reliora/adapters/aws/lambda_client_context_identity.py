"""Resolve trusted Reliora identity from Lambda ClientContext."""

from collections.abc import Mapping

from pydantic import ValidationError

from reliora.adapters.aws.gateway_bug_report_operation import (
    TrustedOperationIdentity,
)


class LambdaClientContextIdentityResolver:
    """Resolve identity supplied through controlled synchronous invocation."""

    def resolve(
        self,
        context: object,
    ) -> TrustedOperationIdentity:
        """Return trusted identifiers from Lambda ClientContext."""

        client_context = getattr(context, "client_context", None)
        custom = getattr(client_context, "custom", None)

        if not isinstance(custom, Mapping):
            raise TypeError(
        "Lambda ClientContext custom identity is required."
         )

        try:
            return TrustedOperationIdentity.model_validate(
                {
                    "operation_id": custom.get("relioraOperationId"),
                    "request_id": custom.get("relioraRequestId"),
                    "session_id": custom.get("relioraSessionId"),
                }
            )
        except ValidationError as error:
            raise ValueError(
                "Lambda ClientContext contains invalid Reliora identity."
            ) from error