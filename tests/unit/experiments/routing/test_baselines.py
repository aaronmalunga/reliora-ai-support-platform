"""Unit tests for simple routing benchmark baselines."""

import pytest

from experiments.routing.benchmark.baselines import (
    B0_TIE_BREAK_ORDER,
    MajorityBaseline,
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