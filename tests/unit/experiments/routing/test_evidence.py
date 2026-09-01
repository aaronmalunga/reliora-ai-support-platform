"""Unit tests for routing benchmark evidence construction."""

from typing import cast

import pytest

from experiments.routing.benchmark.data import (
    Intent,
    RoutingRecord,
)
from experiments.routing.benchmark.evidence import (
    classification_metrics_to_dict,
    collect_failure_cases,
    failure_cases_to_dicts,
)
from experiments.routing.benchmark.metrics import (
    ClassificationMetrics,
    PerClassMetrics,
)


def _synthetic_records() -> tuple[RoutingRecord, ...]:
    """Return synthetic records for evidence-layer unit tests."""

    return (
        RoutingRecord(
            case_id="synthetic-001",
            family_id="family-a",
            variant_id="A",
            message="Checkout crashes when I pay.",
            expected_intent="BUG",
            split="train",
            provenance="SYNTHETIC_TEST_FIXTURE",
        ),
        RoutingRecord(
            case_id="synthetic-002",
            family_id="family-b",
            variant_id="A",
            message="What is your return policy?",
            expected_intent="PLATFORM",
            split="train",
            provenance="SYNTHETIC_TEST_FIXTURE",
        ),
        RoutingRecord(
            case_id="synthetic-003",
            family_id="family-c",
            variant_id="A",
            message="Recommend a science-fiction movie.",
            expected_intent="OTHER",
            split="train",
            provenance="SYNTHETIC_TEST_FIXTURE",
        ),
    )


def test_collect_failure_cases_preserves_only_misclassifications() -> None:
    records = _synthetic_records()
    predictions: tuple[Intent, ...] = (
        "BUG",
        "OTHER",
        "PLATFORM",
    )

    failures = collect_failure_cases(
        records,
        predictions,
    )

    assert len(failures) == 2

    assert failures[0].case_id == "synthetic-002"
    assert failures[0].expected_intent == "PLATFORM"
    assert failures[0].predicted_intent == "OTHER"

    assert failures[1].case_id == "synthetic-003"
    assert failures[1].expected_intent == "OTHER"
    assert failures[1].predicted_intent == "PLATFORM"


def test_collect_failure_cases_preserves_audit_metadata() -> None:
    records = _synthetic_records()
    predictions: tuple[Intent, ...] = (
        "OTHER",
        "PLATFORM",
        "OTHER",
    )

    failures = collect_failure_cases(
        records,
        predictions,
    )

    assert len(failures) == 1

    failure = failures[0]

    assert failure.case_id == "synthetic-001"
    assert failure.family_id == "family-a"
    assert failure.variant_id == "A"
    assert failure.message == "Checkout crashes when I pay."
    assert failure.split == "train"
    assert failure.provenance == "SYNTHETIC_TEST_FIXTURE"


def test_collect_failure_cases_returns_empty_when_all_predictions_match() -> None:
    records = _synthetic_records()
    predictions: tuple[Intent, ...] = (
        "BUG",
        "PLATFORM",
        "OTHER",
    )

    failures = collect_failure_cases(
        records,
        predictions,
    )

    assert failures == ()


def test_collect_failure_cases_rejects_mismatched_counts() -> None:
    records = _synthetic_records()

    with pytest.raises(
        ValueError,
        match="Record and prediction counts must match",
    ):
        collect_failure_cases(
            records,
            ("BUG",),
        )


def test_collect_failure_cases_rejects_unsupported_predictions() -> None:
    records = _synthetic_records()
    unsupported = cast(Intent, "UNKNOWN")

    with pytest.raises(
        ValueError,
        match="unsupported predicted labels",
    ):
        collect_failure_cases(
            records,
            (
                "BUG",
                "PLATFORM",
                unsupported,
            ),
        )


def test_classification_metrics_serialization_preserves_structure() -> None:
    metrics = ClassificationMetrics(
        sample_count=6,
        accuracy=0.5,
        macro_precision=0.55,
        macro_recall=0.5,
        macro_f1=0.48,
        per_class=(
            PerClassMetrics(
                intent="BUG",
                precision=0.5,
                recall=1.0,
                f1=2 / 3,
                support=2,
            ),
            PerClassMetrics(
                intent="PLATFORM",
                precision=0.5,
                recall=0.5,
                f1=0.5,
                support=2,
            ),
            PerClassMetrics(
                intent="OTHER",
                precision=2 / 3,
                recall=0.0,
                f1=0.0,
                support=2,
            ),
        ),
        confusion_matrix=(
            (2, 0, 0),
            (1, 1, 0),
            (1, 1, 0),
        ),
    )

    evidence = classification_metrics_to_dict(metrics)

    assert evidence["sample_count"] == 6
    assert evidence["accuracy"] == 0.5
    assert evidence["macro_f1"] == 0.48

    assert evidence["label_order"] == [
        "BUG",
        "PLATFORM",
        "OTHER",
    ]

    assert evidence["confusion_matrix"] == [
        [2, 0, 0],
        [1, 1, 0],
        [1, 1, 0],
    ]

    assert evidence["per_class"] == [
        {
            "intent": "BUG",
            "precision": 0.5,
            "recall": 1.0,
            "f1": 2 / 3,
            "support": 2,
        },
        {
            "intent": "PLATFORM",
            "precision": 0.5,
            "recall": 0.5,
            "f1": 0.5,
            "support": 2,
        },
        {
            "intent": "OTHER",
            "precision": 2 / 3,
            "recall": 0.0,
            "f1": 0.0,
            "support": 2,
        },
    ]


def test_failure_serialization_preserves_complete_failure_record() -> None:
    records = _synthetic_records()
    predictions: tuple[Intent, ...] = (
        "OTHER",
        "PLATFORM",
        "OTHER",
    )

    failures = collect_failure_cases(
        records,
        predictions,
    )

    serialized = failure_cases_to_dicts(failures)

    assert serialized == [
        {
            "case_id": "synthetic-001",
            "family_id": "family-a",
            "variant_id": "A",
            "message": "Checkout crashes when I pay.",
            "expected_intent": "BUG",
            "predicted_intent": "OTHER",
            "split": "train",
            "provenance": "SYNTHETIC_TEST_FIXTURE",
        }
    ]