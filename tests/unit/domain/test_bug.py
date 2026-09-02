"""Unit tests for Reliora bug-report domain contracts."""

import pytest
from pydantic import ValidationError

from reliora.domain.bug import BugField, BugReportDraft


def test_empty_bug_report_draft_is_incomplete() -> None:
    """FR-007/FR-008: an empty draft is not ready for ticket creation."""

    draft = BugReportDraft()

    assert draft.is_complete is False
    assert draft.missing_fields == (
        BugField.DESCRIPTION,
        BugField.STEPS_TO_REPRODUCE,
        BugField.ENVIRONMENT,
    )


def test_complete_bug_report_draft_has_no_missing_fields() -> None:
    """FR-007: all three required fields satisfy completeness."""

    draft = BugReportDraft(
        description="Checkout crashes when Pay is clicked.",
        steps_to_reproduce="Open cart, continue to checkout, click Pay.",
        environment="Chrome 120 on macOS Sonoma.",
    )

    assert draft.is_complete is True
    assert draft.missing_fields == ()
    assert draft.next_missing_field is None


def test_missing_fields_are_reported_in_defined_collection_order() -> None:
    """FR-008: missing-field discovery is deterministic."""

    draft = BugReportDraft(
        description="Checkout crashes.",
    )

    assert draft.missing_fields == (
        BugField.STEPS_TO_REPRODUCE,
        BugField.ENVIRONMENT,
    )


def test_next_missing_field_returns_only_one_field() -> None:
    """INV-004/FR-008: incremental collection exposes one field per turn."""

    draft = BugReportDraft(
        description="Checkout crashes.",
    )

    assert draft.next_missing_field is BugField.STEPS_TO_REPRODUCE


def test_partial_bug_report_advances_to_next_missing_field() -> None:
    """FR-008: collection state advances as information becomes available."""

    draft = BugReportDraft(
        description="Checkout crashes.",
        steps_to_reproduce="Click Pay after entering card details.",
    )

    assert draft.next_missing_field is BugField.ENVIRONMENT


@pytest.mark.parametrize(
    "field_name",
    [
        "description",
        "steps_to_reproduce",
        "environment",
    ],
)
def test_blank_required_field_is_treated_as_missing(field_name: str) -> None:
    """FR-007/FR-020: blank text does not satisfy a required bug field."""

    draft = BugReportDraft.model_validate({field_name: "   "})

    assert getattr(draft, field_name) is None


def test_bug_report_fields_are_normalized() -> None:
    """FR-020: accepted bug information is normalized at the boundary."""

    draft = BugReportDraft(
        description="   Checkout crashes.   ",
        steps_to_reproduce="   Click Pay.   ",
        environment="   Chrome on Windows 11.   ",
    )

    assert draft.description == "Checkout crashes."
    assert draft.steps_to_reproduce == "Click Pay."
    assert draft.environment == "Chrome on Windows 11."


def test_bug_report_draft_rejects_unexpected_fields() -> None:
    """FR-019/FR-020: undeclared bug data cannot silently enter the contract."""

    with pytest.raises(ValidationError):
        BugReportDraft.model_validate(
            {
                "description": "Checkout crashes.",
                "steps_to_reproduce": "Click Pay.",
                "environment": "Chrome.",
                "priority_override": "critical",
            }
        )


def test_bug_report_draft_is_immutable() -> None:
    """Validated bug-report state cannot be silently mutated."""

    draft = BugReportDraft(
        description="Checkout crashes.",
    )

    with pytest.raises(ValidationError):
        draft.description = "Changed after validation."