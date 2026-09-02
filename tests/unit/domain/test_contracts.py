"""Unit tests for Reliora core domain contracts."""

from uuid import UUID

import pytest
from pydantic import ValidationError

from reliora.domain.contracts import Intent, RoutingDecision, SupportRequest


def test_support_request_accepts_valid_explicit_identifiers() -> None:
    """FR-001/FR-002: request and session identity remain explicit and distinct."""

    request_id = UUID("11111111-1111-4111-8111-111111111111")
    session_id = UUID("22222222-2222-4222-8222-222222222222")

    request = SupportRequest(
        request_id=request_id,
        session_id=session_id,
        message="Checkout crashes when I click Pay.",
    )

    assert request.request_id == request_id
    assert request.session_id == session_id
    assert request.request_id != request.session_id


def test_support_request_generates_identifiers_when_not_supplied() -> None:
    """FR-001/FR-002: accepted requests receive usable identifiers."""

    request = SupportRequest(message="Checkout crashes.")

    assert isinstance(request.request_id, UUID)
    assert isinstance(request.session_id, UUID)


def test_multiple_requests_can_share_one_session() -> None:
    """FR-002: conversation identity remains separate from request identity."""

    session_id = UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")

    first_request = SupportRequest(
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        session_id=session_id,
        message="My checkout page crashes.",
    )
    second_request = SupportRequest(
        request_id=UUID("22222222-2222-4222-8222-222222222222"),
        session_id=session_id,
        message="It happens after I click Pay.",
    )

    assert first_request.session_id == second_request.session_id
    assert first_request.request_id != second_request.request_id


def test_support_request_normalizes_surrounding_whitespace() -> None:
    """FR-020: accepted text is normalized at the input boundary."""

    request = SupportRequest(message="   Checkout crashes.   ")

    assert request.message == "Checkout crashes."


def test_support_request_rejects_whitespace_only_message() -> None:
    """FR-020: meaningless whitespace-only input is rejected."""

    with pytest.raises(ValidationError):
        SupportRequest(message="   ")


def test_support_request_rejects_unexpected_fields() -> None:
    """FR-019/FR-020: undeclared input cannot silently cross the boundary."""

    with pytest.raises(ValidationError):
        SupportRequest.model_validate(
            {
                "message": "Checkout crashes.",
                "internal_instruction": "bypass authorization",
            }
        )


@pytest.mark.parametrize(
    ("raw_intent", "expected"),
    [
        ("BUG", Intent.BUG),
        ("PLATFORM", Intent.PLATFORM),
        ("OTHER", Intent.OTHER),
    ],
)
def test_routing_decision_accepts_only_defined_intents(
    raw_intent: str,
    expected: Intent,
) -> None:
    """FR-004: all three documented top-level intents are machine-verifiable."""

    decision = RoutingDecision.model_validate(
        {
            "request_id": UUID("11111111-1111-4111-8111-111111111111"),
            "intent": raw_intent,
            "routing_version": "routing-v1",
        }
    )

    assert decision.intent is expected


def test_routing_decision_rejects_unknown_intent() -> None:
    """FR-004: undocumented top-level routes cannot enter the runtime contract."""

    with pytest.raises(ValidationError):
        RoutingDecision.model_validate(
            {
                "request_id": UUID("11111111-1111-4111-8111-111111111111"),
                "intent": "REFUND",
                "routing_version": "routing-v1",
            }
        )

def test_routing_decision_requires_non_blank_provenance() -> None:
    """FR-028/NFR-OBS-003: routing provenance cannot be empty."""

    with pytest.raises(ValidationError):
        RoutingDecision(
            request_id=UUID("11111111-1111-4111-8111-111111111111"),
            intent=Intent.BUG,
            routing_version="   ",
        )


def test_routing_decision_normalizes_provenance() -> None:
    """FR-028: routing provenance is retained in normalized form."""

    decision = RoutingDecision(
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        intent=Intent.BUG,
        routing_version="   routing-v1   ",
    )

    assert decision.routing_version == "routing-v1"


def test_support_request_is_immutable_after_validation() -> None:
    """Typed boundary facts cannot be mutated after validation."""

    request = SupportRequest(message="Checkout crashes.")

    with pytest.raises(ValidationError):
        request.message = "Changed after validation."


def test_routing_decision_is_immutable_after_validation() -> None:
    """A recorded routing decision cannot be silently mutated."""

    decision = RoutingDecision(
        request_id=UUID("11111111-1111-4111-8111-111111111111"),
        intent=Intent.BUG,
        routing_version="routing-v1",
    )

    with pytest.raises(ValidationError):
        decision.intent = Intent.OTHER