"""Tests for AgentCore Gateway bug-report input translation."""

import pytest
from pydantic import ValidationError

from reliora.adapters.aws.gateway_bug_report_input import (
    parse_gateway_bug_report,
)


def test_gateway_input_translates_to_domain_field_names() -> None:
    draft = parse_gateway_bug_report(
        {
            "description": "Checkout crashes",
            "stepsToReproduce": "Open cart, then click Pay",
            "environment": "Chrome 120 on macOS",
        }
    )

    assert draft.description == "Checkout crashes"
    assert draft.steps_to_reproduce == "Open cart, then click Pay"
    assert draft.environment == "Chrome 120 on macOS"


def test_gateway_input_rejects_missing_required_tool_field() -> None:
    with pytest.raises(ValidationError):
        parse_gateway_bug_report(
            {
                "description": "Checkout crashes",
                "environment": "Chrome 120 on macOS",
            }
        )


def test_gateway_input_rejects_model_supplied_operation_identity() -> None:
    with pytest.raises(ValidationError):
        parse_gateway_bug_report(
            {
                "description": "Checkout crashes",
                "stepsToReproduce": "Open cart, then click Pay",
                "environment": "Chrome 120 on macOS",
                "operation_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
            }
        )