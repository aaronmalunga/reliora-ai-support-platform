"""Classification metrics for the Reliora routing benchmark."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from sklearn.metrics import (  # type: ignore[import-untyped]
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
)

from experiments.routing.benchmark.data import (
    ALLOWED_INTENTS,
    Intent,
)

LABEL_ORDER: tuple[Intent, ...] = (
    "BUG",
    "PLATFORM",
    "OTHER",
)


@dataclass(frozen=True, slots=True)
class PerClassMetrics:
    """Classification metrics for one routing intent."""

    intent: Intent
    precision: float
    recall: float
    f1: float
    support: int


@dataclass(frozen=True, slots=True)
class ClassificationMetrics:
    """Aggregate and per-class routing classification metrics."""

    sample_count: int
    accuracy: float
    macro_precision: float
    macro_recall: float
    macro_f1: float
    per_class: tuple[PerClassMetrics, ...]
    confusion_matrix: tuple[tuple[int, ...], ...]


def _validate_labels(
    labels: Sequence[Intent],
    *,
    name: str,
) -> None:
    """Reject labels outside the frozen routing contract."""

    unsupported = {
        label
        for label in labels
        if label not in ALLOWED_INTENTS
    }

    if unsupported:
        raise ValueError(
            f"{name} contains unsupported routing labels: "
            f"{sorted(unsupported)!r}."
        )


def calculate_classification_metrics(
    expected: Sequence[Intent],
    predicted: Sequence[Intent],
) -> ClassificationMetrics:
    """Calculate classification metrics using the frozen label order."""

    if not expected:
        raise ValueError(
            "Classification metrics require at least one expected label."
        )

    if len(expected) != len(predicted):
        raise ValueError(
            "Expected and predicted label counts must match: "
            f"{len(expected)} != {len(predicted)}."
        )

    _validate_labels(expected, name="expected")
    _validate_labels(predicted, name="predicted")

    labels = list(LABEL_ORDER)

    macro_precision, macro_recall, macro_f1, _ = (
        precision_recall_fscore_support(
            expected,
            predicted,
            labels=labels,
            average="macro",
            zero_division=0,
        )
    )

    (
        class_precision,
        class_recall,
        class_f1,
        class_support,
    ) = precision_recall_fscore_support(
        expected,
        predicted,
        labels=labels,
        average=None,
        zero_division=0,
    )

    per_class = tuple(
        PerClassMetrics(
            intent=intent,
            precision=float(class_precision[index]),
            recall=float(class_recall[index]),
            f1=float(class_f1[index]),
            support=int(class_support[index]),
        )
        for index, intent in enumerate(LABEL_ORDER)
    )

    matrix = confusion_matrix(
        expected,
        predicted,
        labels=labels,
    )

    frozen_matrix = tuple(
        tuple(
            int(value)
            for value in row
        )
        for row in matrix
    )

    return ClassificationMetrics(
        sample_count=len(expected),
        accuracy=float(
            accuracy_score(
                expected,
                predicted,
            )
        ),
        macro_precision=float(macro_precision),
        macro_recall=float(macro_recall),
        macro_f1=float(macro_f1),
        per_class=per_class,
        confusion_matrix=frozen_matrix,
    )