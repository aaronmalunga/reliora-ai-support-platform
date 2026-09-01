"""Unit tests for classical routing benchmark candidates."""

import pytest

from experiments.routing.benchmark.classical import (
    CLASSICAL_SEARCH_SPACE,
    SEARCH_SPACE_VERSION,
    ClassicalCandidateConfig,
    configurations_for_family,
    fit_classical_candidate,
)
from experiments.routing.benchmark.data import (
    ALLOWED_INTENTS,
    load_routing_records,
    model_examples_for_split,
)


def _configuration(
    candidate_id: str,
) -> ClassicalCandidateConfig:
    """Return one preregistered candidate by ID."""

    return next(
        configuration
        for configuration in CLASSICAL_SEARCH_SPACE
        if configuration.candidate_id == candidate_id
    )


def test_classical_search_space_has_expected_version_and_ids() -> None:
    assert SEARCH_SPACE_VERSION == "1.0.0"

    assert tuple(
        configuration.candidate_id
        for configuration in CLASSICAL_SEARCH_SPACE
    ) == (
        "C1-N1-C0.5",
        "C1-N1-C1.0",
        "C1-N1-C2.0",
        "C1-N2-C0.5",
        "C1-N2-C1.0",
        "C1-N2-C2.0",
        "C2-N1-C0.5",
        "C2-N1-C1.0",
        "C2-N1-C2.0",
        "C2-N2-C0.5",
        "C2-N2-C1.0",
        "C2-N2-C2.0",
    )


def test_classical_search_space_has_six_configurations_per_family() -> None:
    c1_configurations = configurations_for_family("C1")
    c2_configurations = configurations_for_family("C2")

    assert len(CLASSICAL_SEARCH_SPACE) == 12
    assert len(c1_configurations) == 6
    assert len(c2_configurations) == 6


def test_classical_search_space_maps_ngram_and_c_values() -> None:
    for configuration in CLASSICAL_SEARCH_SPACE:
        if "-N1-" in configuration.candidate_id:
            assert configuration.ngram_range == (1, 1)
        else:
            assert configuration.ngram_range == (1, 2)

        assert configuration.c in {
            0.5,
            1.0,
            2.0,
        }


def test_unregistered_classical_configuration_is_rejected() -> None:
    records = load_routing_records()
    training_examples = model_examples_for_split(records, "train")

    unregistered = ClassicalCandidateConfig(
        candidate_id="C1-N1-C9.0",
        family="C1",
        ngram_range=(1, 1),
        c=9.0,
    )

    with pytest.raises(
        ValueError,
        match="not part of the preregistered classical search space",
    ):
        fit_classical_candidate(
            unregistered,
            training_examples,
        )


def test_classical_candidate_rejects_empty_training_data() -> None:
    configuration = _configuration("C1-N1-C1.0")

    with pytest.raises(
        ValueError,
        match="require at least one training example",
    ):
        fit_classical_candidate(
            configuration,
            (),
        )


@pytest.mark.parametrize(
    "candidate_id",
    (
        "C1-N1-C1.0",
        "C2-N2-C1.0",
    ),
)
def test_pipeline_matches_preregistered_configuration(
    candidate_id: str,
) -> None:
    records = load_routing_records()
    training_examples = model_examples_for_split(records, "train")
    configuration = _configuration(candidate_id)

    candidate = fit_classical_candidate(
        configuration,
        training_examples,
    )

    parameters = candidate.pipeline.get_params()

    assert parameters["tfidf__analyzer"] == "word"
    assert parameters["tfidf__lowercase"] is True
    assert parameters["tfidf__strip_accents"] is None
    assert parameters["tfidf__min_df"] == 1
    assert parameters["tfidf__max_df"] == 1.0
    assert parameters["tfidf__norm"] == "l2"
    assert parameters["tfidf__use_idf"] is True
    assert parameters["tfidf__smooth_idf"] is True
    assert parameters["tfidf__sublinear_tf"] is False
    assert parameters["tfidf__stop_words"] is None
    assert parameters["tfidf__ngram_range"] == configuration.ngram_range

    assert parameters["classifier__C"] == configuration.c
    assert parameters["classifier__class_weight"] is None
    assert parameters["classifier__tol"] == pytest.approx(0.0001)

    if configuration.family == "C1":
        assert (
            candidate.pipeline.named_steps[
                "classifier"
            ].__class__.__name__
            == "LogisticRegression"
        )
        assert parameters["classifier__solver"] == "lbfgs"
        assert parameters["classifier__max_iter"] == 1000
        assert parameters["classifier__fit_intercept"] is True
    else:
        assert (
            candidate.pipeline.named_steps[
                "classifier"
            ].__class__.__name__
            == "LinearSVC"
        )
        assert parameters["classifier__max_iter"] == 5000


@pytest.mark.parametrize(
    "candidate_id",
    (
        "C1-N1-C1.0",
        "C2-N1-C1.0",
    ),
)
def test_fitted_candidate_returns_valid_deterministic_predictions(
    candidate_id: str,
) -> None:
    records = load_routing_records()
    training_examples = model_examples_for_split(records, "train")
    configuration = _configuration(candidate_id)

    candidate = fit_classical_candidate(
        configuration,
        training_examples,
    )

    messages = tuple(
        example.message
        for example in training_examples[:12]
    )

    first_predictions = candidate.predict(messages)
    second_predictions = candidate.predict(messages)

    assert len(first_predictions) == len(messages)
    assert first_predictions == second_predictions
    assert set(first_predictions).issubset(ALLOWED_INTENTS)