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
B1_RULESET_VERSION = "1.0.0"

B1_EXTERNAL_RETAILER_SIGNALS = (
    "amazon",
    "ebay",
    "nike",
    "another store",
)

B1_BUG_COMPONENT_SIGNALS = (
    "checkout",
    "payment",
    "pay now",
    "purchase button",
    "sign in",
    "login",
    "log in",
    "cart",
    "quantity",
    "search",
    "coupon",
    "promo",
    "order",
    "address",
    "product page",
    "app",
)

B1_BUG_FAILURE_SIGNALS = (
    "crash",
    "closes",
    "close by itself",
    "freeze",
    "error",
    "broken",
    "does not update",
    "doesn't update",
    "wont change",
    "won't change",
    "nothing sticks",
    "not working",
    "isnt working",
    "isn't working",
    "does nothing",
    "unresponsive",
    "wont respond",
    "won't respond",
    "wont work",
    "won't work",
    "spins forever",
    "loop",
    "sending me back",
    "dumped straight back",
    "keep asking",
    "keeps asking",
    "reverting",
    "disappear",
    "unchanged",
    "nothing changes",
    "stays there",
    "fails to load",
    "fail to load",
    "force closing",
    "stopped working",
    "exit",
)

B1_PLATFORM_SIGNALS = (
    "return policy",
    "return window",
    "sending a purchase back",
    "shipping",
    "delivery",
    "payment method",
    "payment option",
    "debit card",
    "digital wallet",
    "use to pay",
    "warranty",
    "loyalty",
    "reward",
    "membership point",
    "student discount",
    "student pricing",
    "discount for students",
    "countries",
    "cancel",
    "cancelling",
    "change where my order is going",
)

B1_PLATFORM_COMPOUND_SIGNALS = (
    ("return", "item"),
    ("return", "purchase"),
    ("return", "order"),
    ("return", "product"),
    ("order", "arrive"),
    ("order", "deliver"),
    ("student", "discount"),
    ("stop", "order"),
)

B1_PRECEDENCE = (
    "EXTERNAL_RETAILER",
    "BUG",
    "PLATFORM",
    "OTHER_FALLBACK",
)


def _contains_any(
    message: str,
    signals: Sequence[str],
) -> bool:
    """Return whether normalized message text contains any signal."""

    return any(
        signal in message
        for signal in signals
    )


def _contains_all(
    message: str,
    signals: Sequence[str],
) -> bool:
    """Return whether normalized message text contains every signal."""

    return all(
        signal in message
        for signal in signals
    )


@dataclass(frozen=True, slots=True)
class RuleBaseline:
    """B1 deterministic routing-rule baseline."""

    ruleset_version: str = B1_RULESET_VERSION

    def predict_one(
        self,
        message: str,
    ) -> Intent:
        """Classify one customer message using deterministic precedence."""

        normalized = " ".join(
            message.lower().split()
        )

        if _contains_any(
            normalized,
            B1_EXTERNAL_RETAILER_SIGNALS,
        ):
            return "OTHER"

        has_bug_component = _contains_any(
            normalized,
            B1_BUG_COMPONENT_SIGNALS,
        )
        has_bug_failure = _contains_any(
            normalized,
            B1_BUG_FAILURE_SIGNALS,
        )

        if has_bug_component and has_bug_failure:
            return "BUG"

        if _contains_any(
            normalized,
            B1_PLATFORM_SIGNALS,
        ):
            return "PLATFORM"

        if any(
            _contains_all(normalized, signals)
            for signals in B1_PLATFORM_COMPOUND_SIGNALS
        ):
            return "PLATFORM"

        return "OTHER"

    def predict(
        self,
        messages: Sequence[str],
    ) -> tuple[Intent, ...]:
        """Classify customer messages with the frozen B1 ruleset."""

        return tuple(
            self.predict_one(message)
            for message in messages
        )