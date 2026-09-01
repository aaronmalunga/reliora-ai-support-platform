"""Unit tests for routing benchmark classification metrics."""

from typing import cast

import pytest

from experiments.routing.benchmark.data import Intent
from experiments.routing.benchmark.metrics import (
    LABEL_ORDER,
    calculate_classification_metrics,
)


def test_label_order_matches_frozen_routing_contract() -> None:
    assert LABEL_ORDER == (
        "BUG",
        "PLATFORM",
        "OTHER",
    )


def test_perfect_predictions_produce_perfect_metrics() -> None:
    expected: tuple[Intent, ...] = (
        "BUG",
        "PLATFORM",
        "OTHER",
    )
    predicted: tuple[Intent, ...] = expected

    metrics = calculate_classification_metrics(
        expected,
        predicted,
    )

    assert metrics.sample_count == 3
    assert metrics.accuracy == pytest.approx(1.0)
    assert metrics.macro_precision == pytest.approx(1.0)
    assert metrics.macro_recall == pytest.approx(1.0)
    assert metrics.macro_f1 == pytest.approx(1.0)

    assert metrics.confusion_matrix == (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    )

    assert tuple(
        class_metrics.intent
        for class_metrics in metrics.per_class
    ) == LABEL_ORDER

    assert tuple(
        class_metrics.support
        for class_metrics in metrics.per_class
    ) == (
        1,
        1,
        1,
    )


def test_known_confusions_produce_expected_metrics() -> None:
    expected: tuple[Intent, ...] = (
        "BUG",
        "PLATFORM",
        "OTHER",
        "OTHER",
    )
    predicted: tuple[Intent, ...] = (
        "BUG",
        "BUG",
        "OTHER",
        "PLATFORM",
    )

    metrics = calculate_classification_metrics(
        expected,
        predicted,
    )

    assert metrics.sample_count == 4
    assert metrics.accuracy == pytest.approx(0.5)

    assert metrics.macro_precision == pytest.approx(0.5)
    assert metrics.macro_recall == pytest.approx(0.5)
    assert metrics.macro_f1 == pytest.approx(4 / 9)

    assert metrics.confusion_matrix == (
        (1, 0, 0),
        (1, 0, 0),
        (0, 1, 1),
    )

    bug_metrics = metrics.per_class[0]
    platform_metrics = metrics.per_class[1]
    other_metrics = metrics.per_class[2]

    assert bug_metrics.intent == "BUG"
    assert bug_metrics.precision == pytest.approx(0.5)
    assert bug_metrics.recall == pytest.approx(1.0)
    assert bug_metrics.f1 == pytest.approx(2 / 3)
    assert bug_metrics.support == 1

    assert platform_metrics.intent == "PLATFORM"
    assert platform_metrics.precision == pytest.approx(0.0)
    assert platform_metrics.recall == pytest.approx(0.0)
    assert platform_metrics.f1 == pytest.approx(0.0)
    assert platform_metrics.support == 1

    assert other_metrics.intent == "OTHER"
    assert other_metrics.precision == pytest.approx(1.0)
    assert other_metrics.recall == pytest.approx(0.5)
    assert other_metrics.f1 == pytest.approx(2 / 3)
    assert other_metrics.support == 2


def test_missing_predicted_classes_are_scored_as_zero() -> None:
    expected: tuple[Intent, ...] = (
        "BUG",
        "PLATFORM",
        "OTHER",
    )
    predicted: tuple[Intent, ...] = (
        "BUG",
        "BUG",
        "BUG",
    )

    metrics = calculate_classification_metrics(
        expected,
        predicted,
    )

    assert metrics.confusion_matrix == (
        (1, 0, 0),
        (1, 0, 0),
        (1, 0, 0),
    )

    platform_metrics = metrics.per_class[1]
    other_metrics = metrics.per_class[2]

    assert platform_metrics.precision == pytest.approx(0.0)
    assert platform_metrics.recall == pytest.approx(0.0)
    assert platform_metrics.f1 == pytest.approx(0.0)

    assert other_metrics.precision == pytest.approx(0.0)
    assert other_metrics.recall == pytest.approx(0.0)
    assert other_metrics.f1 == pytest.approx(0.0)


def test_empty_expected_labels_are_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Classification metrics require at least one expected label.",
    ):
        calculate_classification_metrics(
            (),
            (),
        )


def test_mismatched_label_counts_are_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Expected and predicted label counts must match",
    ):
        calculate_classification_metrics(
            ("BUG",),
            ("BUG", "OTHER"),
        )


def test_unsupported_expected_label_is_rejected() -> None:
    unsupported = cast(Intent, "UNKNOWN")

    with pytest.raises(
        ValueError,
        match="expected contains unsupported routing labels",
    ):
        calculate_classification_metrics(
            (unsupported,),
            ("BUG",),
        )


def test_unsupported_predicted_label_is_rejected() -> None:
    unsupported = cast(Intent, "UNKNOWN")

    with pytest.raises(
        ValueError,
        match="predicted contains unsupported routing labels",
    ):
        calculate_classification_metrics(
            ("BUG",),
            (unsupported,),
        )