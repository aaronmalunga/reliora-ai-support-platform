"""Measure operational characteristics of shortlisted routing candidates.

This script does not evaluate classification quality and does not access the
validation or held-out test splits for prediction.

Classical candidates are fitted using the frozen training split. Inference
latency and determinism are measured against a fixed synthetic probe set.
"""

from __future__ import annotations

import json
import platform
import statistics
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter_ns
from typing import Protocol

import sklearn  # type: ignore[import-untyped]

from experiments.routing.benchmark.baselines import RuleBaseline
from experiments.routing.benchmark.classical import (
    CLASSICAL_SEARCH_SPACE,
    ClassicalCandidateConfig,
    fit_classical_candidate,
)
from experiments.routing.benchmark.data import (
    ModelExample,
    load_routing_records,
    model_examples_for_split,
)

ROUTING_ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = (
    ROUTING_ROOT
    / "results"
    / "routing-operational-evidence-v1.json"
)

EXPERIMENT_ID = "routing-operational-evidence-v1"
EVIDENCE_CLASSIFICATION = "EXPERIMENTAL"

WARMUP_RUNS = 25
MEASUREMENT_RUNS = 500
TRAINING_RUNS = 10

SHORTLISTED_CLASSICAL_IDS = (
    "C1-N1-C2.0",
    "C2-N1-C2.0",
)

PROBE_MESSAGES = (
    "The checkout button stops working after I enter my card details.",
    "How long does standard shipping normally take?",
    "Tell me how to make vegetable soup.",
    "The mobile app crashes whenever I open my order history.",
    "Can I return an item after opening the package?",
    "Who won the football match yesterday?",
    "My password reset page shows an error.",
    "Do you accept gift cards?",
    "Write a short poem about the ocean.",
    "The link in my delivery email opens a broken page.",
    "When should an approved refund reach my account?",
    "What is the capital of Brazil?",
)


class Predictor(Protocol):
    """Minimal interface required for operational measurement."""

    def predict(
        self,
        messages: tuple[str, ...],
    ) -> tuple[str, ...]:
        """Predict one intent for every supplied message."""


@dataclass(frozen=True)
class LatencySummary:
    """Summary of measured prediction latency."""

    runs: int
    messages_per_run: int
    total_predictions: int
    mean_ms_per_run: float
    p50_ms_per_run: float
    p95_ms_per_run: float
    mean_ms_per_message: float
    p50_ms_per_message: float
    p95_ms_per_message: float


@dataclass(frozen=True)
class TrainingSummary:
    """Summary of repeated classical candidate fitting."""

    runs: int
    mean_ms: float
    p50_ms: float
    p95_ms: float


def percentile(
    values: list[float],
    probability: float,
) -> float:
    """Return a linearly interpolated percentile."""

    if not values:
        raise ValueError("Cannot calculate a percentile from no values.")

    if not 0.0 <= probability <= 1.0:
        raise ValueError(
            "Probability must be between 0.0 and 1.0."
        )

    ordered = sorted(values)

    if len(ordered) == 1:
        return ordered[0]

    position = probability * (len(ordered) - 1)
    lower_index = int(position)
    upper_index = min(
        lower_index + 1,
        len(ordered) - 1,
    )

    fraction = position - lower_index

    return (
        ordered[lower_index]
        + (
            ordered[upper_index]
            - ordered[lower_index]
        )
        * fraction
    )


def measure_latency(
    predictor: Predictor,
    messages: tuple[str, ...],
) -> LatencySummary:
    """Measure warm repeated inference latency."""

    if not messages:
        raise ValueError(
            "Latency measurement requires at least one message."
        )

    for _ in range(WARMUP_RUNS):
        predictor.predict(messages)

    elapsed_ms: list[float] = []

    for _ in range(MEASUREMENT_RUNS):
        started_ns = perf_counter_ns()

        predictions = predictor.predict(messages)

        finished_ns = perf_counter_ns()

        if len(predictions) != len(messages):
            raise ValueError(
                "Predictor returned an unexpected number of predictions."
            )

        elapsed_ms.append(
            (finished_ns - started_ns) / 1_000_000
        )

    message_count = len(messages)

    per_message_ms = [
        duration / message_count
        for duration in elapsed_ms
    ]

    return LatencySummary(
        runs=MEASUREMENT_RUNS,
        messages_per_run=message_count,
        total_predictions=(
            MEASUREMENT_RUNS
            * message_count
        ),
        mean_ms_per_run=statistics.fmean(
            elapsed_ms
        ),
        p50_ms_per_run=percentile(
            elapsed_ms,
            0.50,
        ),
        p95_ms_per_run=percentile(
            elapsed_ms,
            0.95,
        ),
        mean_ms_per_message=statistics.fmean(
            per_message_ms
        ),
        p50_ms_per_message=percentile(
            per_message_ms,
            0.50,
        ),
        p95_ms_per_message=percentile(
            per_message_ms,
            0.95,
        ),
    )


def verify_prediction_determinism(
    predictor: Predictor,
    messages: tuple[str, ...],
    *,
    repetitions: int = 100,
) -> bool:
    """Return whether repeated predictions remain identical."""

    if repetitions < 2:
        raise ValueError(
            "Determinism verification requires at least two repetitions."
        )

    reference = predictor.predict(messages)

    for _ in range(repetitions - 1):
        if predictor.predict(messages) != reference:
            return False

    return True


def configuration_by_id(
    candidate_id: str,
) -> ClassicalCandidateConfig:
    """Return one configuration from the frozen search space."""

    matches = tuple(
        configuration
        for configuration in CLASSICAL_SEARCH_SPACE
        if configuration.candidate_id == candidate_id
    )

    if len(matches) != 1:
        raise ValueError(
            "Expected exactly one frozen configuration for "
            f"{candidate_id!r}; found {len(matches)}."
        )

    return matches[0]


def measure_training(
    configuration: ClassicalCandidateConfig,
    training_examples: Sequence[ModelExample],
) -> TrainingSummary:
    """Measure repeated classical candidate fitting time."""

    elapsed_ms: list[float] = []

    for _ in range(TRAINING_RUNS):
        started_ns = perf_counter_ns()

        fit_classical_candidate(
            configuration,
            training_examples,
        )

        finished_ns = perf_counter_ns()

        elapsed_ms.append(
            (finished_ns - started_ns) / 1_000_000
        )

    return TrainingSummary(
        runs=TRAINING_RUNS,
        mean_ms=statistics.fmean(
            elapsed_ms
        ),
        p50_ms=percentile(
            elapsed_ms,
            0.50,
        ),
        p95_ms=percentile(
            elapsed_ms,
            0.95,
        ),
    )


def latency_to_dict(
    summary: LatencySummary,
) -> dict[str, object]:
    """Serialize latency evidence."""

    return {
        "warmup_runs": WARMUP_RUNS,
        "measurement_runs": summary.runs,
        "messages_per_run": summary.messages_per_run,
        "total_predictions": summary.total_predictions,
        "mean_ms_per_run": summary.mean_ms_per_run,
        "p50_ms_per_run": summary.p50_ms_per_run,
        "p95_ms_per_run": summary.p95_ms_per_run,
        "mean_ms_per_message": summary.mean_ms_per_message,
        "p50_ms_per_message": summary.p50_ms_per_message,
        "p95_ms_per_message": summary.p95_ms_per_message,
    }


def training_to_dict(
    summary: TrainingSummary,
) -> dict[str, object]:
    """Serialize training-time evidence."""

    return {
        "runs": summary.runs,
        "mean_ms": summary.mean_ms,
        "p50_ms": summary.p50_ms,
        "p95_ms": summary.p95_ms,
    }


def run_operational_measurement() -> dict[str, object]:
    """Measure shortlisted candidates without opening validation or test."""

    records = load_routing_records()

    training_examples = model_examples_for_split(
        records,
        "train",
    )

    candidate_results: list[dict[str, object]] = []

    rule_baseline = RuleBaseline()

    candidate_results.append(
        {
            "candidate_id": "B1",
            "family": "DETERMINISTIC_RULE_BASELINE",
            "training_required": False,
            "training_latency": None,
            "prediction_deterministic": (
                verify_prediction_determinism(
                    rule_baseline,
                    PROBE_MESSAGES,
                )
            ),
            "inference_latency": latency_to_dict(
                measure_latency(
                    rule_baseline,
                    PROBE_MESSAGES,
                )
            ),
        }
    )

    for candidate_id in SHORTLISTED_CLASSICAL_IDS:
        configuration = configuration_by_id(
            candidate_id
        )

        training_summary = measure_training(
            configuration,
            training_examples,
        )

        fitted_candidate = fit_classical_candidate(
            configuration,
            training_examples,
        )

        candidate_results.append(
            {
                "candidate_id": candidate_id,
                "family": configuration.family,
                "training_required": True,
                "training_latency": training_to_dict(
                    training_summary
                ),
                "prediction_deterministic": (
                    verify_prediction_determinism(
                        fitted_candidate,
                        PROBE_MESSAGES,
                    )
                ),
                "inference_latency": latency_to_dict(
                    measure_latency(
                        fitted_candidate,
                        PROBE_MESSAGES,
                    )
                ),
            }
        )

    return {
        "experiment_id": EXPERIMENT_ID,
        "evidence_classification": EVIDENCE_CLASSIFICATION,
        "experiment_timestamp_utc": datetime.now(
            UTC
        ).isoformat(),
        "environment": {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "scikit_learn_version": sklearn.__version__,
            "timer": "time.perf_counter_ns",
        },
        "measurement_protocol": {
            "training_split_used_for_fitting": True,
            "validation_split_used": False,
            "held_out_test_used": False,
            "probe_provenance": "SYNTHETIC_OPERATIONAL_PROBE",
            "probe_message_count": len(
                PROBE_MESSAGES
            ),
            "warmup_runs": WARMUP_RUNS,
            "measurement_runs": MEASUREMENT_RUNS,
            "training_runs": TRAINING_RUNS,
            "determinism_repetitions": 100,
            "latency_scope": (
                "local in-process routing inference only"
            ),
            "excluded_from_latency": (
                "network, AWS, API, serialization, queueing, "
                "cold-start, and downstream tool latency"
            ),
        },
        "shortlist": [
            "B1",
            *SHORTLISTED_CLASSICAL_IDS,
        ],
        "candidates": candidate_results,
    }


def write_report(
    report: dict[str, object],
    path: Path = RESULT_PATH,
) -> None:
    """Write operational evidence as formatted JSON."""

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
    """Run the operational measurement."""

    try:
        report = run_operational_measurement()
        write_report(report)
    except (
        OSError,
        TypeError,
        ValueError,
    ) as error:
        print(
            f"Routing operational measurement failed: {error}"
        )
        return 1

    candidates = report["candidates"]

    if not isinstance(candidates, list):
        print(
            "Routing operational measurement failed: "
            "report candidates are not a list."
        )
        return 1

    print("Routing operational measurement completed")
    print(
        f"Experiment: {report['experiment_id']}"
    )
    print(
        "Candidates: "
        f"{len(candidates)}"
    )
    print("Validation split used: False")
    print("Held-out test used: False")
    print(f"Report: {RESULT_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())