"""Unit tests for customer-visible internal-information leakage."""

from reliora.evaluation.leakage import (
    evaluate_internal_information_leakage,
)


def test_clean_customer_response_passes() -> None:
    response = (
        "I don't have enough approved information to answer that question. "
        "I can direct you to customer support for further assistance."
    )

    result = evaluate_internal_information_leakage(response)

    assert result.passed is True
    assert result.invariant_id == "INV-012"
    assert result.evidence["matches"] == {}


def test_internal_handoff_route_label_fails() -> None:
    response = (
        "HUMAN HANDOFF: I don't have enough information to answer that. "
        "Please contact customer support."
    )

    result = evaluate_internal_information_leakage(response)

    assert result.passed is False
    assert "human_handoff_route" in result.evidence["matches"]


def test_thinking_tag_fails() -> None:
    response = (
        "<thinking>I should call the bug-report tool.</thinking>"
        "Your ticket has been created."
    )

    result = evaluate_internal_information_leakage(response)

    assert result.passed is False
    assert "thinking_tag" in result.evidence["matches"]


def test_case_insensitive_thinking_tag_fails() -> None:
    response = "<THINKING>Internal reasoning.</THINKING> Please wait."

    result = evaluate_internal_information_leakage(response)

    assert result.passed is False
    assert "thinking_tag" in result.evidence["matches"]