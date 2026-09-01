"""Unit tests for the routing benchmark runner."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import experiments.routing.scripts.run_routing_benchmark as runner
from experiments.routing.benchmark.classical import (
    CLASSICAL_SEARCH_SPACE,
    ClassicalCandidateConfig,
)
from experiments.routing.benchmark.data import RoutingRecord


def _configuration(
    candidate_id: str,
) -> ClassicalCandidateConfig:
    """Return one frozen classical configuration by ID."""

    return next(
        configuration
        for configuration in CLASSICAL_SEARCH_SPACE
        if configuration.candidate_id == candidate_id
    )


def _synthetic_benchmark_records() -> tuple[RoutingRecord, ...]:
    """Return synthetic train and validation records for runner tests."""

    return (
        RoutingRecord(
            case_id="train-bug",
            family_id="train-family-bug",
            variant_id="A",
            message="Checkout crashes when I pay.",
            expected_intent="BUG",
            split="train",
            provenance="SYNTHETIC_TEST_FIXTURE",
        ),
        RoutingRecord(
            case_id="train-platform",
            family_id="train-family-platform",
            variant_id="A",
            message="What is your return policy?",
            expected_intent="PLATFORM",
            split="train",
            provenance="SYNTHETIC_TEST_FIXTURE",
        ),
        RoutingRecord(
            case_id="train-other",
            family_id="train-family-other",
            variant_id="A",
            message="Recommend a science fiction movie.",
            expected_intent="OTHER",
            split="train",
            provenance="SYNTHETIC_TEST_FIXTURE",
        ),
        RoutingRecord(
            case_id="validation-bug",
            family_id="validation-family-bug",
            variant_id="A",
            message="The app keeps crashing.",
            expected_intent="BUG",
            split="validation",
            provenance="SYNTHETIC_TEST_FIXTURE",
        ),
        RoutingRecord(
            case_id="validation-platform",
            family_id="validation-family-platform",
            variant_id="A",
            message="How long does shipping take?",
            expected_intent="PLATFORM",
            split="validation",
            provenance="SYNTHETIC_TEST_FIXTURE",
        ),
        RoutingRecord(
            case_id="validation-other",
            family_id="validation-family-other",
            variant_id="A",
            message="What is the capital of Argentina?",
            expected_intent="OTHER",
            split="validation",
            provenance="SYNTHETIC_TEST_FIXTURE",
        ),
    )


def test_canonical_lf_sha256_normalizes_line_endings(
    tmp_path: Path,
) -> None:
    lf_path = tmp_path / "lf.txt"
    crlf_path = tmp_path / "crlf.txt"

    lf_path.write_bytes(
        b"alpha\nbeta\n"
    )
    crlf_path.write_bytes(
        b"alpha\r\nbeta\r\n"
    )

    expected = hashlib.sha256(
        b"alpha\nbeta\n"
    ).hexdigest()

    assert runner.canonical_lf_sha256(lf_path) == expected
    assert runner.canonical_lf_sha256(crlf_path) == expected


def test_evaluate_predictions_preserves_metrics_and_failures() -> None:
    records = _synthetic_benchmark_records()[3:]

    result = runner.evaluate_predictions(
        candidate_id="SYNTHETIC",
        family="TEST_FIXTURE",
        configuration={
            "purpose": "unit-test",
        },
        records=records,
        predictions=(
            "BUG",
            "OTHER",
            "OTHER",
        ),
    )

    assert result["candidate_id"] == "SYNTHETIC"
    assert result["family"] == "TEST_FIXTURE"
    assert result["failure_count"] == 1

    metrics = result["metrics"]

    assert isinstance(metrics, dict)
    assert metrics["sample_count"] == 3
    assert metrics["accuracy"] == pytest.approx(2 / 3)

    failures = result["failures"]

    assert isinstance(failures, list)
    assert len(failures) == 1

    failure = failures[0]

    assert failure["case_id"] == "validation-platform"
    assert failure["expected_intent"] == "PLATFORM"
    assert failure["predicted_intent"] == "OTHER"


def test_logistic_configuration_serialization_matches_contract() -> None:
    configuration = _configuration(
        "C1-N2-C2.0"
    )

    serialized = runner.classical_configuration_to_dict(
        configuration
    )

    assert serialized["search_space_version"] == "1.0.0"
    assert serialized["ngram_range"] == [1, 2]
    assert serialized["C"] == 2.0

    classifier = serialized["classifier"]

    assert isinstance(classifier, dict)
    assert classifier["name"] == "LogisticRegression"
    assert classifier["solver"] == "lbfgs"
    assert classifier["max_iter"] == 1000
    assert classifier["class_weight"] is None
    assert classifier["fit_intercept"] is True
    assert classifier["tol"] == pytest.approx(0.0001)


def test_svm_configuration_serialization_matches_contract() -> None:
    configuration = _configuration(
        "C2-N1-C0.5"
    )

    serialized = runner.classical_configuration_to_dict(
        configuration
    )

    assert serialized["search_space_version"] == "1.0.0"
    assert serialized["ngram_range"] == [1, 1]
    assert serialized["C"] == 0.5

    classifier = serialized["classifier"]

    assert isinstance(classifier, dict)
    assert classifier["name"] == "LinearSVC"
    assert classifier["max_iter"] == 5000
    assert classifier["class_weight"] is None
    assert classifier["tol"] == pytest.approx(0.0001)


def test_write_report_creates_json_with_final_newline(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "report.json"

    report: dict[str, object] = {
        "experiment_id": "synthetic-test",
        "candidate_count": 2,
        "held_out_test_used": False,
    }

    runner.write_report(
        report,
        output_path,
    )

    raw = output_path.read_bytes()

    assert raw.endswith(b"\n")

    loaded = json.loads(
        output_path.read_text(
            encoding="utf-8"
        )
    )

    assert loaded == report


def test_validation_runner_uses_synthetic_records_only(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records = _synthetic_benchmark_records()

    monkeypatch.setattr(
        runner,
        "load_routing_records",
        lambda: records,
    )
    monkeypatch.setattr(
        runner,
        "canonical_lf_sha256",
        lambda path: runner.EXPECTED_DATASET_CANONICAL_SHA256,
    )
    monkeypatch.setattr(
        runner,
        "git_revision",
        lambda: "synthetic-git-revision",
    )

    report = runner.run_validation_benchmark()

    assert report["experiment_id"] == (
        "routing-benchmark-validation-v1"
    )
    assert report["evidence_classification"] == "EXPERIMENTAL"
    assert report["benchmark_git_revision"] == (
        "synthetic-git-revision"
    )
    assert report["candidate_count"] == 14

    split_usage = report["split_usage"]

    assert isinstance(split_usage, dict)

    training = split_usage["training"]
    evaluation = split_usage["evaluation"]
    held_out = split_usage["held_out_test"]

    assert isinstance(training, dict)
    assert isinstance(evaluation, dict)
    assert isinstance(held_out, dict)

    assert training["split"] == "train"
    assert training["record_count"] == 3

    assert evaluation["split"] == "validation"
    assert evaluation["record_count"] == 3

    assert held_out["split"] == "test"
    assert held_out["used"] is False

    candidates = report["candidates"]

    assert isinstance(candidates, list)
    assert len(candidates) == 14

    candidate_ids = {
        candidate["candidate_id"]
        for candidate in candidates
    }

    assert candidate_ids == {
        "B0",
        "B1",
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
    }


def test_runner_result_path_is_inside_routing_results_directory() -> None:
    assert runner.RESULT_PATH.parent == (
        runner.ROUTING_ROOT / "results"
    )
    assert runner.RESULT_PATH.name == (
        "routing-benchmark-validation-v1.json"
    )