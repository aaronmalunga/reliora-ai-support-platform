"""Unit tests for the final routing held-out test runner."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import experiments.routing.scripts.run_routing_held_out_test as runner


class SyntheticCandidate:
    """Minimal fitted candidate used by orchestration tests."""

    def predict(
        self,
        messages: tuple[str, ...],
    ) -> tuple[str, ...]:
        return tuple(
            "BUG"
            for _ in messages
        )


def test_selected_configuration_is_frozen_c2_candidate() -> None:
    configuration = runner.selected_configuration()

    assert configuration.candidate_id == "C2-N1-C2.0"
    assert configuration.family == "C2"


def test_selected_configuration_rejects_missing_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        runner,
        "CLASSICAL_SEARCH_SPACE",
        (),
    )

    with pytest.raises(
        ValueError,
        match="Expected exactly one selected routing configuration",
    ):
        runner.selected_configuration()


def test_dataset_hash_mismatch_stops_before_data_loading(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        runner,
        "canonical_lf_sha256",
        lambda path: "unexpected-hash",
    )

    dataset_loaded = False

    def fake_load_routing_records() -> tuple[object, ...]:
        nonlocal dataset_loaded
        dataset_loaded = True
        return ()

    monkeypatch.setattr(
        runner,
        "load_routing_records",
        fake_load_routing_records,
    )

    with pytest.raises(
        ValueError,
        match="Frozen routing dataset hash mismatch",
    ):
        runner.run_held_out_test()

    assert dataset_loaded is False


def test_held_out_runner_uses_train_and_test_but_not_validation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requested_training_splits: list[str] = []
    requested_evaluation_splits: list[str] = []

    synthetic_training_examples = (
        object(),
        object(),
    )

    synthetic_test_records = (
        type(
            "SyntheticRecord",
            (),
            {
                "message": "Synthetic bug message one",
            },
        )(),
        type(
            "SyntheticRecord",
            (),
            {
                "message": "Synthetic bug message two",
            },
        )(),
    )

    monkeypatch.setattr(
        runner,
        "canonical_lf_sha256",
        lambda path: runner.EXPECTED_DATASET_CANONICAL_SHA256,
    )

    monkeypatch.setattr(
        runner,
        "load_routing_records",
        lambda: ("synthetic-dataset",),
    )

    def fake_model_examples_for_split(
        records: object,
        split: str,
    ) -> tuple[object, ...]:
        del records

        requested_training_splits.append(
            split
        )

        return synthetic_training_examples

    def fake_records_for_split(
        records: object,
        split: str,
    ) -> tuple[object, ...]:
        del records

        requested_evaluation_splits.append(
            split
        )

        return synthetic_test_records

    monkeypatch.setattr(
        runner,
        "model_examples_for_split",
        fake_model_examples_for_split,
    )

    monkeypatch.setattr(
        runner,
        "records_for_split",
        fake_records_for_split,
    )

    monkeypatch.setattr(
        runner,
        "fit_classical_candidate",
        lambda configuration, training_examples: SyntheticCandidate(),
    )

    monkeypatch.setattr(
        runner,
        "evaluate_predictions",
        lambda **kwargs: {
            "candidate_id": "C2-N1-C2.0",
            "family": "C2",
            "metrics": {
                "accuracy": 1.0,
                "macro_f1": 1.0,
            },
            "failure_count": 0,
            "failures": [],
        },
    )

    monkeypatch.setattr(
        runner,
        "git_revision",
        lambda: "synthetic-test-revision",
    )

    report = runner.run_held_out_test()

    assert requested_training_splits == [
        "train",
    ]

    assert requested_evaluation_splits == [
        "test",
    ]

    split_usage = report["split_usage"]

    assert isinstance(
        split_usage,
        dict,
    )

    validation = split_usage["validation"]
    held_out = split_usage["held_out_test"]

    assert isinstance(
        validation,
        dict,
    )
    assert isinstance(
        held_out,
        dict,
    )

    assert validation["used"] is False
    assert held_out["used"] is True
    assert held_out["record_count"] == 2


def test_held_out_runner_records_selection_firewall(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        runner,
        "canonical_lf_sha256",
        lambda path: runner.EXPECTED_DATASET_CANONICAL_SHA256,
    )

    monkeypatch.setattr(
        runner,
        "load_routing_records",
        lambda: ("synthetic-dataset",),
    )

    monkeypatch.setattr(
        runner,
        "model_examples_for_split",
        lambda records, split: (object(),),
    )

    synthetic_record = type(
        "SyntheticRecord",
        (),
        {
            "message": "Synthetic bug message",
        },
    )()

    monkeypatch.setattr(
        runner,
        "records_for_split",
        lambda records, split: (
            synthetic_record,
        ),
    )

    monkeypatch.setattr(
        runner,
        "fit_classical_candidate",
        lambda configuration, training_examples: SyntheticCandidate(),
    )

    monkeypatch.setattr(
        runner,
        "evaluate_predictions",
        lambda **kwargs: {
            "candidate_id": "C2-N1-C2.0",
            "family": "C2",
            "metrics": {
                "accuracy": 1.0,
                "macro_f1": 1.0,
            },
            "failure_count": 0,
            "failures": [],
        },
    )

    monkeypatch.setattr(
        runner,
        "git_revision",
        lambda: "synthetic-test-revision",
    )

    report = runner.run_held_out_test()

    selection = report["selection"]

    assert isinstance(
        selection,
        dict,
    )

    assert selection["decision_id"] == "ROUTING-SELECTION-V1"
    assert selection["selection_decision_commit"] == "fd47277"
    assert selection["selected_candidate_id"] == "C2-N1-C2.0"
    assert selection["configuration_search_performed"] is False
    assert (
        selection["selection_changed_after_test_exposure"]
        is False
    )


def test_write_report_creates_json_with_final_newline(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "held-out.json"

    report: dict[str, object] = {
        "experiment_id": "synthetic-held-out-test",
        "selected_candidate": "C2-N1-C2.0",
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


def test_result_path_is_dedicated_to_held_out_evidence() -> None:
    assert runner.RESULT_PATH.parent == (
        runner.ROUTING_ROOT / "results"
    )

    assert runner.RESULT_PATH.name == (
        "routing-held-out-test-v1.json"
    )