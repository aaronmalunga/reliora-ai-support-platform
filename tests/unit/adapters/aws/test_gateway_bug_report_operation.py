"""Tests for trusted AgentCore Gateway operation construction."""

from uuid import UUID

from reliora.adapters.aws.gateway_bug_report_operation import (
    TrustedOperationIdentity,
    build_gateway_bug_report_operation,
)

OPERATION_ID = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
FIRST_REQUEST_ID = UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")
SECOND_REQUEST_ID = UUID("cccccccc-cccc-4ccc-8ccc-cccccccccccc")
SESSION_ID = UUID("dddddddd-dddd-4ddd-8ddd-dddddddddddd")


def _gateway_event() -> dict[str, str]:
    return {
        "description": "Checkout crashes",
        "stepsToReproduce": "Open cart, then click Pay",
        "environment": "Chrome 120 on macOS",
    }


def test_gateway_operation_preserves_trusted_identifiers() -> None:
    identity = TrustedOperationIdentity(
        operation_id=OPERATION_ID,
        request_id=FIRST_REQUEST_ID,
        session_id=SESSION_ID,
    )

    operation = build_gateway_bug_report_operation(
        _gateway_event(),
        identity=identity,
    )

    assert operation.operation_id == OPERATION_ID
    assert operation.request_id == FIRST_REQUEST_ID
    assert operation.session_id == SESSION_ID
    assert operation.bug_report.steps_to_reproduce == (
        "Open cart, then click Pay"
    )


def test_retry_can_reuse_operation_id_with_new_request_id() -> None:
    first_attempt = build_gateway_bug_report_operation(
        _gateway_event(),
        identity=TrustedOperationIdentity(
            operation_id=OPERATION_ID,
            request_id=FIRST_REQUEST_ID,
            session_id=SESSION_ID,
        ),
    )

    retry_attempt = build_gateway_bug_report_operation(
        _gateway_event(),
        identity=TrustedOperationIdentity(
            operation_id=OPERATION_ID,
            request_id=SECOND_REQUEST_ID,
            session_id=SESSION_ID,
        ),
    )

    assert first_attempt.operation_id == retry_attempt.operation_id
    assert first_attempt.request_id != retry_attempt.request_id
    assert first_attempt.session_id == retry_attempt.session_id