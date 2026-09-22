"""AWS Lambda entrypoint for Reliora bug-ticket execution."""

import os

import boto3

from reliora.adapters.aws.dynamodb_ticket_execution import (
    DynamoDBTicketExecutionCoordinator,
)
from reliora.adapters.aws.lambda_bug_report_runtime import (
    LambdaBugReportRuntime,
)
from reliora.adapters.aws.lambda_client_context_identity import (
    LambdaClientContextIdentityResolver,
)

_RUNTIME: LambdaBugReportRuntime | None = None


def _required_environment_variable(name: str) -> str:
    value = os.environ.get(name)

    if not value:
        raise RuntimeError(
            f"Required Lambda environment variable is missing: {name}"
        )

    return value


def _build_runtime() -> LambdaBugReportRuntime:
    dynamodb = boto3.client("dynamodb")

    execution = DynamoDBTicketExecutionCoordinator(
        dynamodb_client=dynamodb,
        operations_table_name=_required_environment_variable(
            "RELIORA_OPERATIONS_TABLE"
        ),
        tickets_table_name=_required_environment_variable(
            "RELIORA_TICKETS_TABLE"
        ),
    )

    return LambdaBugReportRuntime(
        ticket_execution=execution,
        identity_resolver=LambdaClientContextIdentityResolver(),
    )


def lambda_handler(
    event: dict[str, object],
    context: object,
) -> dict[str, object]:
    """Execute one Reliora bug-ticket Lambda invocation."""

    global _RUNTIME

    if _RUNTIME is None:
        _RUNTIME = _build_runtime()

    return _RUNTIME.handle(event, context)