"""Classical statistical candidates for the Reliora routing benchmark."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Literal, cast

from sklearn.feature_extraction.text import (  # type: ignore[import-untyped]
    TfidfVectorizer,
)
from sklearn.linear_model import LogisticRegression  # type: ignore[import-untyped]
from sklearn.pipeline import Pipeline  # type: ignore[import-untyped]
from sklearn.svm import LinearSVC  # type: ignore[import-untyped]

from experiments.routing.benchmark.data import (
    ALLOWED_INTENTS,
    Intent,
    ModelExample,
)

CandidateFamily = Literal["C1", "C2"]

SEARCH_SPACE_VERSION = "1.0.0"

C_VALUES: tuple[float, ...] = (
    0.5,
    1.0,
    2.0,
)

NGRAM_CONFIGURATIONS: tuple[
    tuple[str, tuple[int, int]],
    ...,
] = (
    ("N1", (1, 1)),
    ("N2", (1, 2)),
)


@dataclass(frozen=True, slots=True)
class ClassicalCandidateConfig:
    """One preregistered classical routing candidate configuration."""

    candidate_id: str
    family: CandidateFamily
    ngram_range: tuple[int, int]
    c: float


def _build_search_space() -> tuple[ClassicalCandidateConfig, ...]:
    """Construct the frozen 12-configuration classical search space."""

    configurations: list[ClassicalCandidateConfig] = []

    for family in ("C1", "C2"):
        for ngram_id, ngram_range in NGRAM_CONFIGURATIONS:
            for c_value in C_VALUES:
                configurations.append(
                    ClassicalCandidateConfig(
                        candidate_id=(
                            f"{family}-{ngram_id}-C{c_value:.1f}"
                        ),
                        family=family,
                        ngram_range=ngram_range,
                        c=c_value,
                    )
                )

    return tuple(configurations)


CLASSICAL_SEARCH_SPACE = _build_search_space()


def configurations_for_family(
    family: CandidateFamily,
) -> tuple[ClassicalCandidateConfig, ...]:
    """Return preregistered configurations for one candidate family."""

    return tuple(
        configuration
        for configuration in CLASSICAL_SEARCH_SPACE
        if configuration.family == family
    )


def _build_vectorizer(
    configuration: ClassicalCandidateConfig,
) -> Any:
    """Build TF-IDF preprocessing from the frozen search-space contract."""

    return TfidfVectorizer(
        analyzer="word",
        lowercase=True,
        strip_accents=None,
        min_df=1,
        max_df=1.0,
        norm="l2",
        use_idf=True,
        smooth_idf=True,
        sublinear_tf=False,
        stop_words=None,
        ngram_range=configuration.ngram_range,
    )


def _build_classifier(
    configuration: ClassicalCandidateConfig,
) -> Any:
    """Build the classifier for one preregistered candidate."""

    if configuration.family == "C1":
        return LogisticRegression(
            C=configuration.c,
            solver="lbfgs",
            max_iter=1000,
            class_weight=None,
            fit_intercept=True,
            tol=0.0001,
        )

    return LinearSVC(
        C=configuration.c,
        class_weight=None,
        max_iter=5000,
        tol=0.0001,
    )


def _build_pipeline(
    configuration: ClassicalCandidateConfig,
) -> Any:
    """Construct a TF-IDF plus classifier pipeline."""

    return Pipeline(
        steps=(
            (
                "tfidf",
                _build_vectorizer(configuration),
            ),
            (
                "classifier",
                _build_classifier(configuration),
            ),
        )
    )


@dataclass(slots=True)
class FittedClassicalCandidate:
    """One fitted classical routing candidate."""

    configuration: ClassicalCandidateConfig
    pipeline: Any

    def predict(
        self,
        messages: Sequence[str],
    ) -> tuple[Intent, ...]:
        """Predict routing labels for customer messages."""

        raw_predictions = self.pipeline.predict(
            list(messages)
        )

        predictions = tuple(
            str(prediction)
            for prediction in raw_predictions
        )

        unsupported = {
            prediction
            for prediction in predictions
            if prediction not in ALLOWED_INTENTS
        }

        if unsupported:
            raise ValueError(
                "Classical candidate produced unsupported routing labels: "
                f"{sorted(unsupported)!r}."
            )

        return cast(
            tuple[Intent, ...],
            predictions,
        )


def fit_classical_candidate(
    configuration: ClassicalCandidateConfig,
    training_examples: Sequence[ModelExample],
) -> FittedClassicalCandidate:
    """Fit one preregistered classical candidate using training data."""

    if configuration not in CLASSICAL_SEARCH_SPACE:
        raise ValueError(
            "Configuration is not part of the preregistered "
            "classical search space."
        )

    if not training_examples:
        raise ValueError(
            "Classical candidates require at least one training example."
        )

    messages = [
        example.message
        for example in training_examples
    ]

    targets = [
        example.expected_intent
        for example in training_examples
    ]

    pipeline = _build_pipeline(configuration)

    pipeline.fit(
        messages,
        targets,
    )

    return FittedClassicalCandidate(
        configuration=configuration,
        pipeline=pipeline,
    )