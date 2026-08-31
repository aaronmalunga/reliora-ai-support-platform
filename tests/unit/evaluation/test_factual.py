"""Unit tests for deterministic factual-completeness evaluation."""

from reliora.evaluation.factual import evaluate_required_fact_completeness

RETURN_POLICY_FACTS = {
    "return_window": ["30 days"],
    "unused_condition": ["unused"],
    "original_packaging_condition": ["original packaging"],
    "defective_item_exception": ["defective", "damaged", "faulty"],
}


def test_complete_response_passes() -> None:
    result = evaluate_required_fact_completeness(
        response=(
            "Most items can be returned within 30 days when unused and in "
            "original packaging, unless the item arrived defective."
        ),
        required_facts=RETURN_POLICY_FACTS,
    )

    assert result.passed is True
    assert result.evaluation_id == "FACT-001"
    assert result.evidence["missing_facts"] == []


def test_missing_required_exception_fails() -> None:
    result = evaluate_required_fact_completeness(
        response=(
            "You can return most items within 30 days of delivery as long "
            "as they’re unused and in original packaging."
        ),
        required_facts=RETURN_POLICY_FACTS,
    )

    assert result.passed is False
    assert result.evidence["missing_facts"] == [
        "defective_item_exception"
    ]


def test_alternative_accepted_pattern_passes() -> None:
    result = evaluate_required_fact_completeness(
        response=(
            "Returns are accepted within 30 days when products are unused "
            "and in original packaging. Damaged items are an exception."
        ),
        required_facts=RETURN_POLICY_FACTS,
    )

    assert result.passed is True


def test_matching_is_case_insensitive() -> None:
    result = evaluate_required_fact_completeness(
        response=(
            "Returns are allowed within 30 DAYS when UNUSED and in "
            "ORIGINAL PACKAGING, unless the item is DEFECTIVE."
        ),
        required_facts=RETURN_POLICY_FACTS,
    )

    assert result.passed is True