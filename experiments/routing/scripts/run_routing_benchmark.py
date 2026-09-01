"""Run the Reliora routing candidate comparison on validation data."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sklearn  # type: ignore[import-untyped]

from experiments.routing.benchmark.baselines import (
    B0_TIE_BREAK_ORDER,
    B1_PRECEDENCE,
    B1_RULESET_VERSION,
    RuleBaseline,
    fit_majority_baseline,
)
from experiments.routing.benchmark.classical import (
    CLASSICAL_SEARCH_SPACE,
    SEARCH_SPACE_VERSION,
    ClassicalCandidateConfig,
    fit_classical_candidate,
)
from experiments.routing.benchmark.data import (
    DATASET_PATH,
    EXPECTED_DATASET_ID,
    EXPECTED_DATASET_STATUS,
    EXPECTED_DATASET_VERSION,
    Intent,
    RoutingRecord,
    load_routing_records,
    model_examples_for_split,
    records_for_split,
)
from experiments.routing.benchmark.evidence import (
    classification_metrics_to_dict,
    collect_failure_cases,
    failure_cases_to_dicts,
)
from experiments.routing.benchmark.metrics import (
    calculate_classification_metrics,
)

ROUTING_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROUTING_ROOT.parents[1]

RESULT_PATH = (
    ROUTING_ROOT
    / "results"
    / "routing-benchmark-validation-v1.json"
)

EXPECTED_DATASET_CANONICAL_SHA256 = (
    "369600abb8711dcadc0acb96bd19edc33"
    "a9c06a83cf7c09208bccb6dbde85450"
)

EVIDENCE_CLASSIFICATION = "EXPERIMENTAL"
EXPERIMENT_ID = "routing-benchmark-validation-v1"


def canonical_lf_sha256(path: Path) -> str:
    """Hash file bytes after normalizing line endings to LF."""

    data = path.read_bytes()
    normalized = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

    return hashlib.sha256(normalized).hexdigest()


def git_revision() -> str:
    """Return the repository Git revision used for the experiment."""

    completed = subprocess.run(
        (
            "git",
            "rev-parse",
            "HEAD",
        ),
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    return completed.stdout.strip()


def evaluate_predictions(
    *,
    candidate_id: str,
    family: str,
    configuration: dict[str, object],
    records: tuple[RoutingRecord, ...],
    predictions: tuple[Intent, ...],
) -> dict[str, object]:
    """Build metrics and failure evidence for one candidate."""

    expected = tuple(
        record.expected_intent
        for record in records
    )

    metrics = calculate_classification_metrics(
        expected,
        predictions,
    )

    failures = collect_failure_cases(
        records,
        predictions,
    )

    return {
        "candidate_id": candidate_id,
        "family": family,
        "configuration": configuration,
        "metrics": classification_metrics_to_dict(metrics),
        "failure_count": len(failures),
        "failures": failure_cases_to_dicts(failures),
    }


def classical_configuration_to_dict(
    configuration: ClassicalCandidateConfig,
) -> dict[str, object]:
    """Serialize one preregistered classical configuration."""

    common: dict[str, object] = {
        "search_space_version": SEARCH_SPACE_VERSION,
        "ngram_range": list(configuration.ngram_range),
        "C": configuration.c,
        "tfidf": {
            "analyzer": "word",
            "lowercase": True,
            "strip_accents": None,
            "min_df": 1,
            "max_df": 1.0,
            "norm": "l2",
            "use_idf": True,
            "smooth_idf": True,
            "sublinear_tf": False,
            "stop_words": None,
        },
    }

    if configuration.family == "C1":
        common["classifier"] = {
            "name": "LogisticRegression",
            "solver": "lbfgs",
            "max_iter": 1000,
            "class_weight": None,
            "fit_intercept": True,
            "tol": 0.0001,
        }
    else:
        common["classifier"] = {
            "name": "LinearSVC",
            "max_iter": 5000,
            "class_weight": None,
            "tol": 0.0001,
        }

    return common


def run_validation_benchmark() -> dict[str, object]:
    """Run all frozen routing candidates against validation data."""

    dataset_hash = canonical_lf_sha256(DATASET_PATH)

    if dataset_hash != EXPECTED_DATASET_CANONICAL_SHA256:
        raise ValueError(
            "Frozen routing dataset hash mismatch: "
            f"expected {EXPECTED_DATASET_CANONICAL_SHA256}, "
            f"received {dataset_hash}."
        )

    records = load_routing_records()

    training_examples = model_examples_for_split(
        records,
        "train",
    )

    validation_records = records_for_split(
        records,
        "validation",
    )

    validation_messages = tuple(
        record.message
        for record in validation_records
    )

    candidate_results: list[dict[str, object]] = []

    majority_baseline = fit_majority_baseline(
        training_examples
    )

    majority_predictions = majority_baseline.predict(
        validation_messages
    )

    candidate_results.append(
        evaluate_predictions(
            candidate_id="B0",
            family="MAJORITY_BASELINE",
            configuration={
                "predicted_intent": (
                    majority_baseline.predicted_intent
                ),
                "class_counts": [
                    {
                        "intent": intent,
                        "count": count,
                    }
                    for intent, count
                    in majority_baseline.class_counts
                ],
                "tie_break_order": list(
                    B0_TIE_BREAK_ORDER
                ),
            },
            records=validation_records,
            predictions=majority_predictions,
        )
    )

    rule_baseline = RuleBaseline()

    rule_predictions = rule_baseline.predict(
        validation_messages
    )

    candidate_results.append(
        evaluate_predictions(
            candidate_id="B1",
            family="DETERMINISTIC_RULE_BASELINE",
            configuration={
                "ruleset_version": B1_RULESET_VERSION,
                "precedence": list(B1_PRECEDENCE),
                "fallback": "OTHER",
            },
            records=validation_records,
            predictions=rule_predictions,
        )
    )

    for configuration in CLASSICAL_SEARCH_SPACE:
        candidate = fit_classical_candidate(
            configuration,
            training_examples,
        )

        predictions = candidate.predict(
            validation_messages
        )

        candidate_results.append(
            evaluate_predictions(
                candidate_id=configuration.candidate_id,
                family=configuration.family,
                configuration=(
                    classical_configuration_to_dict(
                        configuration
                    )
                ),
                records=validation_records,
                predictions=predictions,
            )
        )

    return {
        "experiment_id": EXPERIMENT_ID,
        "evidence_classification": EVIDENCE_CLASSIFICATION,
        "experiment_timestamp_utc": datetime.now(
            UTC
        ).isoformat(),
        "benchmark_git_revision": git_revision(),
        "dataset": {
            "dataset_id": EXPECTED_DATASET_ID,
            "version": EXPECTED_DATASET_VERSION,
            "status": EXPECTED_DATASET_STATUS,
            "canonical_lf_sha256": dataset_hash,
        },
        "split_usage": {
            "training": {
                "split": "train",
                "record_count": len(training_examples),
                "purpose": "candidate fitting or construction",
            },
            "evaluation": {
                "split": "validation",
                "record_count": len(validation_records),
                "purpose": "candidate and configuration comparison",
            },
            "held_out_test": {
                "split": "test",
                "used": False,
                "purpose": (
                    "reserved for final independent evaluation "
                    "after preferred configuration is fixed"
                ),
            },
        },
        "environment": {
            "python": platform.python_version(),
            "scikit_learn": sklearn.__version__,
        },
        "candidate_count": len(candidate_results),
        "candidates": candidate_results,
    }


def write_report(
    report: dict[str, object],
    path: Path = RESULT_PATH,
) -> None:
    """Write benchmark evidence as deterministic formatted JSON."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    """Run the validation benchmark and return a process exit code."""

    try:
        report = run_validation_benchmark()
        write_report(report)
    except (
        OSError,
        subprocess.CalledProcessError,
        TypeError,
        ValueError,
    ) as exc:
        print("Routing benchmark FAILED")
        print(f"Reason: {exc}")
        return 1

    print("Routing benchmark completed")
    print(f"Experiment: {EXPERIMENT_ID}")
    print(f"Candidates: {report['candidate_count']}")
    print("Evaluation split: validation")
    print("Held-out test used: False")
    print(f"Report: {RESULT_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())