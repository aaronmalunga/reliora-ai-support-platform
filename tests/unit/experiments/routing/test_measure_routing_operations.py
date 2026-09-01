"""Unit tests for routing operational measurement."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import experiments.routing.scripts.measure_routing_operations as operations


class StablePredictor:
    """Predictor that always returns the same outputs."""

    def predict(
        self,
        messages: tuple[str, ...],
    ) -> tuple[str, ...]:
        return tuple(
            "OTHER"
            for _ in messages
        )


class AlternatingPredictor:
    """Predictor whose outputs change between calls."""

    def __init__(self) -> None:
        self._call_count = 0

    def predict(
        self,
        messages: tuple[str, ...],
    ) -> tuple[str, ...]:
        self._call_count += 1

        intent = (
            "OTHER"
            if self._call_count % 2
            else "BUG"
        )

        return tuple(
            intent
            for _ in messages
        )


def test_percentile_returns_expected_interpolated_values() -> None:
    values = [
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
    ]

    assert operations.percentile(
        values,
        0.0,
    ) == pytest.approx(1.0)

    assert operations.percentile(
        values,
        0.5,
    ) == pytest.approx(3.0)

    assert operations.percentile(
        values,
        0.95,
    ) == pytest.approx(4.8)

    assert operations.percentile(
        values,
        1.0,
    ) == pytest.approx(5.0)


def test_percentile_rejects_invalid_inputs() -> None:
    with pytest.raises(
        ValueError,
        match="no values",
    ):
        operations.percentile(
            [],
            0.5,
        )

    with pytest.raises(
        ValueError,
        match="between 0.0 and 1.0",
    ):
        operations.percentile(
            [1.0],
            1.1,
        )


def test_determinism_checker_accepts_stable_predictions() -> None:
    predictor = StablePredictor()

    assert operations.verify_prediction_determinism(
        predictor,
        (
            "First message",
            "Second message",
        ),
        repetitions=5,
    )


def test_determinism_checker_detects_changing_predictions() -> None:
    predictor = AlternatingPredictor()

    assert not operations.verify_prediction_determinism(
        predictor,
        (
            "First message",
            "Second message",
        ),
        repetitions=5,
    )


def test_determinism_checker_rejects_too_few_repetitions() -> None:
    with pytest.raises(
        ValueError,
        match="at least two repetitions",
    ):
        operations.verify_prediction_determinism(
            StablePredictor(),
            ("message",),
            repetitions=1,
        )


def test_configuration_lookup_uses_frozen_search_space() -> None:
    configuration = operations.configuration_by_id(
        "C2-N1-C2.0"
    )

    assert configuration.candidate_id == "C2-N1-C2.0"
    assert configuration.family == "C2"


def test_configuration_lookup_rejects_unknown_candidate() -> None:
    with pytest.raises(
        ValueError,
        match="Expected exactly one frozen configuration",
    ):
        operations.configuration_by_id(
            "C2-N9-C99.0"
        )


def test_latency_measurement_records_expected_workload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        operations,
        "WARMUP_RUNS",
        2,
    )
    monkeypatch.setattr(
        operations,
        "MEASUREMENT_RUNS",
        3,
    )

    predictor = StablePredictor()

    messages = (
        "First",
        "Second",
        "Third",
    )

    summary = operations.measure_latency(
        predictor,
        messages,
    )

    assert summary.runs == 3
    assert summary.messages_per_run == 3
    assert summary.total_predictions == 9

    assert summary.mean_ms_per_run >= 0.0
    assert summary.p50_ms_per_run >= 0.0
    assert summary.p95_ms_per_run >= 0.0

    assert summary.mean_ms_per_message >= 0.0
    assert summary.p50_ms_per_message >= 0.0
    assert summary.p95_ms_per_message >= 0.0


def test_latency_measurement_rejects_empty_probe_set() -> None:
    with pytest.raises(
        ValueError,
        match="at least one message",
    ):
        operations.measure_latency(
            StablePredictor(),
            (),
        )


def test_write_report_creates_json_with_final_newline(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "operations.json"

    report: dict[str, object] = {
        "experiment_id": "synthetic-operational-test",
        "validation_split_used": False,
        "held_out_test_used": False,
    }

    operations.write_report(
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


def test_operational_runner_uses_training_split_only(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requested_splits: list[str] = []

    synthetic_training_examples: tuple[object, ...] = (
        object(),
    )

    monkeypatch.setattr(
        operations,
        "load_routing_records",
        lambda: ("synthetic-record",),
    )

    def fake_model_examples_for_split(
        records: object,
        split: str,
    ) -> tuple[object, ...]:
        del records

        requested_splits.append(
            split
        )

        return synthetic_training_examples

    monkeypatch.setattr(
        operations,
        "model_examples_for_split",
        fake_model_examples_for_split,
    )

    monkeypatch.setattr(
        operations,
        "measure_training",
        lambda configuration, training_examples: (
            operations.TrainingSummary(
                runs=10,
                mean_ms=1.0,
                p50_ms=1.0,
                p95_ms=1.0,
            )
        ),
    )

    monkeypatch.setattr(
        operations,
        "fit_classical_candidate",
        lambda configuration, training_examples: (
            StablePredictor()
        ),
    )

    monkeypatch.setattr(
        operations,
        "verify_prediction_determinism",
        lambda predictor, messages, repetitions=100: True,
    )

    monkeypatch.setattr(
        operations,
        "measure_latency",
        lambda predictor, messages: (
            operations.LatencySummary(
                runs=500,
                messages_per_run=len(messages),
                total_predictions=500 * len(messages),
                mean_ms_per_run=1.0,
                p50_ms_per_run=1.0,
                p95_ms_per_run=1.0,
                mean_ms_per_message=0.1,
                p50_ms_per_message=0.1,
                p95_ms_per_message=0.1,
            )
        ),
    )

    report = operations.run_operational_measurement()

    assert requested_splits == [
        "train",
    ]

    protocol = report["measurement_protocol"]

    assert isinstance(
        protocol,
        dict,
    )

    assert (
        protocol["training_split_used_for_fitting"]
        is True
    )
    assert protocol["validation_split_used"] is False
    assert protocol["held_out_test_used"] is False

    assert report["shortlist"] == [
        "B1",
        "C1-N1-C2.0",
        "C2-N1-C2.0",
    ]

    candidates = report["candidates"]

    assert isinstance(
        candidates,
        list,
    )
    assert len(candidates) == 3

    assert [
        candidate["candidate_id"]
        for candidate in candidates
    ] == [
        "B1",
        "C1-N1-C2.0",
        "C2-N1-C2.0",
    ]