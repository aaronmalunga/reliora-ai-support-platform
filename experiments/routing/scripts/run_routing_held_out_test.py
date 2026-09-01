"""Run the selected routing candidate once against held-out test data.

The routing candidate was selected and frozen before this runner was created.

This runner:
- fits only the selected C2-N1-C2.0 configuration;
- fits using the frozen training split;
- evaluates only the held-out test split;
- does not use validation;
- performs no configuration search or model selection.
"""

from __future__ import annotations

import json
import platform
from datetime import UTC, datetime
from pathlib import Path

import sklearn  # type: ignore[import-untyped]

from experiments.routing.benchmark.classical import (
    CLASSICAL_SEARCH_SPACE,
    ClassicalCandidateConfig,
    fit_classical_candidate,
)
from experiments.routing.benchmark.data import (
    DATASET_PATH,
    EXPECTED_DATASET_ID,
    EXPECTED_DATASET_STATUS,
    EXPECTED_DATASET_VERSION,
    load_routing_records,
    model_examples_for_split,
    records_for_split,
)
from experiments.routing.scripts.run_routing_benchmark import (
    canonical_lf_sha256,
    classical_configuration_to_dict,
    evaluate_predictions,
    git_revision,
)

ROUTING_ROOT = Path(__file__).resolve().parents[1]

RESULT_PATH = (
    ROUTING_ROOT
    / "results"
    / "routing-held-out-test-v1.json"
)

EXPERIMENT_ID = "routing-held-out-test-v1"
EVIDENCE_CLASSIFICATION = "EXPERIMENTAL"

SELECTED_CANDIDATE_ID = "C2-N1-C2.0"

SELECTION_DECISION_ID = "ROUTING-SELECTION-V1"
SELECTION_DECISION_COMMIT = (
    "fd47277"
)

EXPECTED_DATASET_CANONICAL_SHA256 = (
    "369600abb8711dcadc0acb96bd19edc33"
    "a9c06a83cf7c09208bccb6dbde85450"
)


def selected_configuration() -> ClassicalCandidateConfig:
    """Return the configuration frozen by the selection decision."""

    matches = tuple(
        configuration
        for configuration in CLASSICAL_SEARCH_SPACE
        if configuration.candidate_id == SELECTED_CANDIDATE_ID
    )

    if len(matches) != 1:
        raise ValueError(
            "Expected exactly one selected routing configuration; "
            f"found {len(matches)} for {SELECTED_CANDIDATE_ID!r}."
        )

    return matches[0]


def run_held_out_test() -> dict[str, object]:
    """Evaluate the frozen selected candidate on held-out test once."""

    dataset_hash = canonical_lf_sha256(
        DATASET_PATH
    )

    if dataset_hash != EXPECTED_DATASET_CANONICAL_SHA256:
        raise ValueError(
            "Frozen routing dataset hash mismatch: "
            f"expected {EXPECTED_DATASET_CANONICAL_SHA256}, "
            f"observed {dataset_hash}."
        )

    records = load_routing_records()

    training_examples = model_examples_for_split(
        records,
        "train",
    )

    test_records = records_for_split(
        records,
        "test",
    )

    test_messages = tuple(
        record.message
        for record in test_records
    )

    configuration = selected_configuration()

    candidate = fit_classical_candidate(
        configuration,
        training_examples,
    )

    predictions = candidate.predict(
        test_messages
    )

    candidate_result = evaluate_predictions(
        candidate_id=configuration.candidate_id,
        family=configuration.family,
        configuration=classical_configuration_to_dict(
            configuration
        ),
        records=test_records,
        predictions=predictions,
    )

    return {
        "experiment_id": EXPERIMENT_ID,
        "evidence_classification": EVIDENCE_CLASSIFICATION,
        "experiment_timestamp_utc": datetime.now(
            UTC
        ).isoformat(),
        "benchmark_git_revision": git_revision(),
        "selection": {
            "decision_id": SELECTION_DECISION_ID,
            "selection_decision_commit": (
                SELECTION_DECISION_COMMIT
            ),
            "selected_candidate_id": (
                SELECTED_CANDIDATE_ID
            ),
            "configuration_search_performed": False,
            "selection_changed_after_test_exposure": False,
        },
        "dataset": {
            "dataset_id": EXPECTED_DATASET_ID,
            "version": EXPECTED_DATASET_VERSION,
            "status": EXPECTED_DATASET_STATUS,
            "canonical_lf_sha256": dataset_hash,
        },
        "split_usage": {
            "training": {
                "split": "train",
                "record_count": len(
                    training_examples
                ),
                "purpose": (
                    "fit already-selected candidate"
                ),
            },
            "validation": {
                "split": "validation",
                "used": False,
            },
            "held_out_test": {
                "split": "test",
                "record_count": len(
                    test_records
                ),
                "used": True,
                "purpose": (
                    "single final generalization evaluation"
                ),
            },
        },
        "environment": {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "scikit_learn_version": sklearn.__version__,
        },
        "candidate": candidate_result,
    }


def write_report(
    report: dict[str, object],
    path: Path = RESULT_PATH,
) -> None:
    """Write held-out test evidence as formatted JSON."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            report,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    """Run the held-out test evaluation."""

    try:
        report = run_held_out_test()
        write_report(
            report
        )
    except (
        OSError,
        TypeError,
        ValueError,
    ) as error:
        print(
            f"Routing held-out test failed: {error}"
        )
        return 1

    candidate = report["candidate"]

    if not isinstance(
        candidate,
        dict,
    ):
        print(
            "Routing held-out test failed: "
            "candidate result is not a dictionary."
        )
        return 1

    metrics = candidate["metrics"]

    if not isinstance(
        metrics,
        dict,
    ):
        print(
            "Routing held-out test failed: "
            "candidate metrics are not a dictionary."
        )
        return 1

    print("Routing held-out test completed")
    print(
        f"Experiment: {report['experiment_id']}"
    )
    print(
        f"Selected candidate: {SELECTED_CANDIDATE_ID}"
    )
    print("Configuration search performed: False")
    print("Validation split used: False")
    print("Held-out test used: True")
    print(
        "Test accuracy: "
        f"{metrics['accuracy']}"
    )
    print(
        "Test macro F1: "
        f"{metrics['macro_f1']}"
    )
    print(
        "Failures: "
        f"{candidate['failure_count']}"
    )
    print(
        f"Report: {RESULT_PATH}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )