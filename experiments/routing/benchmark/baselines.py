"""Simple baseline candidates for the Reliora routing benchmark."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass

from experiments.routing.benchmark.data import Intent, ModelExample

B0_TIE_BREAK_ORDER: tuple[Intent, ...] = (
    "BUG",
    "PLATFORM",
    "OTHER",
)


@dataclass(frozen=True, slots=True)
class MajorityBaseline:
    """Fitted B0 majority-class routing baseline."""

    predicted_intent: Intent
    class_counts: tuple[tuple[Intent, int], ...]
    tie_break_order: tuple[Intent, ...] = B0_TIE_BREAK_ORDER

    def predict(
        self,
        messages: Sequence[str],
    ) -> tuple[Intent, ...]:
        """Predict the fitted majority intent for every message."""

        return tuple(
            self.predicted_intent
            for _ in messages
        )


def fit_majority_baseline(
    training_examples: Sequence[ModelExample],
) -> MajorityBaseline:
    """Fit B0 from training labels using deterministic tie resolution."""

    if not training_examples:
        raise ValueError(
            "B0 requires at least one training example."
        )

    counts = Counter(
        example.expected_intent
        for example in training_examples
    )

    highest_count = max(counts.values())

    tied_intents = {
        intent
        for intent, count in counts.items()
        if count == highest_count
    }

    selected_intent = next(
        intent
        for intent in B0_TIE_BREAK_ORDER
        if intent in tied_intents
    )

    ordered_counts = tuple(
        (intent, counts.get(intent, 0))
        for intent in B0_TIE_BREAK_ORDER
    )

    return MajorityBaseline(
        predicted_intent=selected_intent,
        class_counts=ordered_counts,
    )