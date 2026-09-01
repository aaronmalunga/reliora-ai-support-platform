"""Unit tests for simple routing benchmark baselines."""

import pytest

from experiments.routing.benchmark.baselines import (
    B0_TIE_BREAK_ORDER,
    B1_PRECEDENCE,
    B1_RULESET_VERSION,
    MajorityBaseline,
    RuleBaseline,
    fit_majority_baseline,
)
from experiments.routing.benchmark.data import (
    ModelExample,
    load_routing_records,
    model_examples_for_split,
)


def test_majority_baseline_rejects_empty_training_data() -> None:
    with pytest.raises(
        ValueError,
        match="B0 requires at least one training example.",
    ):
        fit_majority_baseline(())


def test_majority_baseline_selects_genuine_majority() -> None:
    training_examples = (
        ModelExample(message="a", expected_intent="PLATFORM"),
        ModelExample(message="b", expected_intent="PLATFORM"),
        ModelExample(message="c", expected_intent="BUG"),
    )

    baseline = fit_majority_baseline(training_examples)

    assert baseline.predicted_intent == "PLATFORM"


def test_majority_baseline_uses_declared_tie_break_order() -> None:
    training_examples = (
        ModelExample(message="a", expected_intent="BUG"),
        ModelExample(message="b", expected_intent="PLATFORM"),
        ModelExample(message="c", expected_intent="OTHER"),
    )

    baseline = fit_majority_baseline(training_examples)

    assert B0_TIE_BREAK_ORDER == (
        "BUG",
        "PLATFORM",
        "OTHER",
    )
    assert baseline.predicted_intent == "BUG"


def test_majority_baseline_predicts_same_fitted_class_for_all_messages() -> None:
    baseline = MajorityBaseline(
        predicted_intent="OTHER",
        class_counts=(
            ("BUG", 1),
            ("PLATFORM", 1),
            ("OTHER", 2),
        ),
    )

    predictions = baseline.predict(
        (
            "first customer message",
            "second customer message",
            "third customer message",
        )
    )

    assert predictions == (
        "OTHER",
        "OTHER",
        "OTHER",
    )


def test_frozen_training_split_produces_documented_b0_tie() -> None:
    records = load_routing_records()
    training_examples = model_examples_for_split(records, "train")

    baseline = fit_majority_baseline(training_examples)

    assert baseline.class_counts == (
        ("BUG", 36),
        ("PLATFORM", 36),
        ("OTHER", 36),
    )
    assert baseline.predicted_intent == "BUG"


def test_rule_baseline_exposes_frozen_version_and_precedence() -> None:
    baseline = RuleBaseline()

    assert baseline.ruleset_version == "1.0.0"
    assert B1_RULESET_VERSION == "1.0.0"
    assert B1_PRECEDENCE == (
        "EXTERNAL_RETAILER",
        "BUG",
        "PLATFORM",
        "OTHER_FALLBACK",
    )


def test_rule_baseline_routes_application_failure_to_bug() -> None:
    baseline = RuleBaseline()

    assert (
        baseline.predict_one(
            "The checkout page crashes whenever I try to pay."
        )
        == "BUG"
    )


def test_rule_baseline_requires_failure_signal_for_bug() -> None:
    baseline = RuleBaseline()

    assert (
        baseline.predict_one(
            "Which payment methods do you accept?"
        )
        == "PLATFORM"
    )


def test_rule_baseline_routes_supported_policy_question_to_platform() -> None:
    baseline = RuleBaseline()

    assert (
        baseline.predict_one(
            "How long is the return window for an item?"
        )
        == "PLATFORM"
    )


def test_rule_baseline_external_retailer_override_routes_other() -> None:
    baseline = RuleBaseline()

    assert (
        baseline.predict_one(
            "What is Amazon's return policy?"
        )
        == "OTHER"
    )


def test_rule_baseline_does_not_treat_programming_return_as_platform() -> None:
    baseline = RuleBaseline()

    assert (
        baseline.predict_one(
            "Help me debug a SQL query that returns duplicate rows."
        )
        == "OTHER"
    )


def test_rule_baseline_handles_log_in_wording_as_bug_component() -> None:
    baseline = RuleBaseline()

    assert (
        baseline.predict_one(
            "The site keeps asking me to log in again."
        )
        == "BUG"
    )


def test_rule_baseline_uses_other_as_deterministic_fallback() -> None:
    baseline = RuleBaseline()

    assert (
        baseline.predict_one(
            "What is the capital of Argentina?"
        )
        == "OTHER"
    )


def test_rule_baseline_predicts_multiple_messages_in_order() -> None:
    baseline = RuleBaseline()

    predictions = baseline.predict(
        (
            "Checkout crashes when I press Pay.",
            "What is your return policy?",
            "Recommend a science-fiction movie.",
        )
    )

    assert predictions == (
        "BUG",
        "PLATFORM",
        "OTHER",
    )


def test_frozen_training_split_is_fully_classified_by_b1() -> None:
    records = load_routing_records()
    training_examples = model_examples_for_split(records, "train")

    baseline = RuleBaseline()
    predictions = baseline.predict(
        tuple(
            example.message
            for example in training_examples
        )
    )

    expected = tuple(
        example.expected_intent
        for example in training_examples
    )

    assert predictions == expected