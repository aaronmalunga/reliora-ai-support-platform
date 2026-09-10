"""Tests for controlled Lambda ClientContext identity resolution."""

from uuid import UUID

import pytest

from reliora.adapters.aws.lambda_client_context_identity import (
    LambdaClientContextIdentityResolver,
)

OPERATION_ID = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
REQUEST_ID = UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")
SESSION_ID = UUID("cccccccc-cccc-4ccc-8ccc-cccccccccccc")


class FakeClientContext:
    """Small stand-in for Lambda ClientContext."""

    def __init__(self, custom: dict[str, str]) -> None:
        self.custom = custom


class FakeLambdaContext:
    """Small stand-in for the Lambda runtime context."""

    def __init__(self, custom: dict[str, str]) -> None:
        self.client_context = FakeClientContext(custom)


def test_resolver_reads_controlled_client_context_identity() -> None:
    context = FakeLambdaContext(
        {
            "relioraOperationId": str(OPERATION_ID),
            "relioraRequestId": str(REQUEST_ID),
            "relioraSessionId": str(SESSION_ID),
        }
    )

    identity = LambdaClientContextIdentityResolver().resolve(context)

    assert identity.operation_id == OPERATION_ID
    assert identity.request_id == REQUEST_ID
    assert identity.session_id == SESSION_ID


def test_resolver_rejects_missing_client_context() -> None:
    context = object()

    with pytest.raises(
        TypeError,
        match="ClientContext custom identity is required",
    ):
        LambdaClientContextIdentityResolver().resolve(context)


def test_resolver_rejects_invalid_identity() -> None:
    context = FakeLambdaContext(
        {
            "relioraOperationId": "not-a-uuid",
            "relioraRequestId": str(REQUEST_ID),
            "relioraSessionId": str(SESSION_ID),
        }
    )

    with pytest.raises(
        ValueError,
        match="contains invalid Reliora identity",
    ):
        LambdaClientContextIdentityResolver().resolve(context)