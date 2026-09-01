"""Evidence structures for the Reliora routing benchmark."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from experiments.routing.benchmark.data import (
    ALLOWED_INTENTS,
    Intent,
    RoutingRecord,
    Split,
)
from experiments.routing.benchmark.metrics import (
    LABEL_ORDER,
    ClassificationMetrics,
)


@dataclass(frozen=True, slots=True)
class FailureCase:
    """One preserved routing misclassification."""

    case_id: str
    family_id: str
    variant_id: str
    message: str
    expected_intent: Intent
    predicted_intent: Intent
    split: Split
    provenance: str


def collect_failure_cases(
    records: Sequence[RoutingRecord],
    predictions: Sequence[Intent],
) -> tuple[FailureCase, ...]:
    """Preserve every misclassified record for failure analysis."""

    if len(records) != len(predictions):
        raise ValueError(
            "Record and prediction counts must match: "
            f"{len(records)} != {len(predictions)}."
        )

    unsupported = {
        prediction
        for prediction in predictions
        if prediction not in ALLOWED_INTENTS
    }

    if unsupported:
        raise ValueError(
            "Failure evidence contains unsupported predicted labels: "
            f"{sorted(unsupported)!r}."
        )

    return tuple(
        FailureCase(
            case_id=record.case_id,
            family_id=record.family_id,
            variant_id=record.variant_id,
            message=record.message,
            expected_intent=record.expected_intent,
            predicted_intent=prediction,
            split=record.split,
            provenance=record.provenance,
        )
        for record, prediction in zip(
            records,
            predictions,
            strict=True,
        )
        if record.expected_intent != prediction
    )


def classification_metrics_to_dict(
    metrics: ClassificationMetrics,
) -> dict[str, object]:
    """Convert classification metrics into JSON-ready evidence."""

    return {
        "sample_count": metrics.sample_count,
        "accuracy": metrics.accuracy,
        "macro_precision": metrics.macro_precision,
        "macro_recall": metrics.macro_recall,
        "macro_f1": metrics.macro_f1,
        "label_order": list(LABEL_ORDER),
        "per_class": [
            {
                "intent": class_metrics.intent,
                "precision": class_metrics.precision,
                "recall": class_metrics.recall,
                "f1": class_metrics.f1,
                "support": class_metrics.support,
            }
            for class_metrics in metrics.per_class
        ],
        "confusion_matrix": [
            list(row)
            for row in metrics.confusion_matrix
        ],
    }


def failure_cases_to_dicts(
    failures: Sequence[FailureCase],
) -> list[dict[str, object]]:
    """Convert preserved failures into JSON-ready evidence."""

    return [
        {
            "case_id": failure.case_id,
            "family_id": failure.family_id,
            "variant_id": failure.variant_id,
            "message": failure.message,
            "expected_intent": failure.expected_intent,
            "predicted_intent": failure.predicted_intent,
            "split": failure.split,
            "provenance": failure.provenance,
        }
        for failure in failures
    ]