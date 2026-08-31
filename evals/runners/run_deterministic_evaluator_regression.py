"""Run the deterministic evaluator regression dataset."""

import hashlib
import json
from pathlib import Path
from typing import Any

from reliora.evaluation.regression import evaluate_regression_case

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "evals"
    / "datasets"
    / "deterministic-evaluator-regression-v1.json"
)

REPORT_PATH = (
    PROJECT_ROOT
    / "evidence"
    / "generated"
    / "deterministic-evaluator-regression-v1-report.json"
)

HASH_BASIS = "UTF-8 text normalized to LF line endings before SHA-256"


def normalize_text_bytes_for_hashing(raw_bytes: bytes) -> bytes:
    """Normalize UTF-8 text to LF line endings before hashing."""

    text = raw_bytes.decode("utf-8")
    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")

    return normalized_text.encode("utf-8")


def load_dataset(path: Path) -> tuple[dict[str, Any], str]:
    """Load the regression dataset and return its canonical SHA-256."""

    raw_bytes = path.read_bytes()
    canonical_bytes = normalize_text_bytes_for_hashing(raw_bytes)

    dataset_sha256 = hashlib.sha256(canonical_bytes).hexdigest()
    dataset = json.loads(canonical_bytes.decode("utf-8"))

    return dataset, dataset_sha256


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    """Execute one regression fixture and compare it with expectation."""

    finding = evaluate_regression_case(case)

    expected_passed = case["expected_evaluator_passed"]
    expectation_met = finding.passed == expected_passed

    return {
        "case_id": case["case_id"],
        "title": case["title"],
        "evaluation_id": finding.evaluation_id,
        "case_type": case["case_type"],
        "status": "PASS" if expectation_met else "MISMATCH",
        "expectation_met": expectation_met,
        "expected_evaluator_passed": expected_passed,
        "evaluator_passed": finding.passed,
        "message": finding.message,
        "evidence": finding.evidence,
    }


def build_evaluation_summary(
    results: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Summarize results independently for each evaluator."""

    summary: dict[str, dict[str, Any]] = {}

    for result in results:
        evaluation_id = result["evaluation_id"]

        if evaluation_id not in summary:
            summary[evaluation_id] = {
                "total_cases": 0,
                "matched_expectations": 0,
                "mismatches": 0,
            }

        evaluator_summary = summary[evaluation_id]
        evaluator_summary["total_cases"] += 1

        if result["expectation_met"]:
            evaluator_summary["matched_expectations"] += 1
        else:
            evaluator_summary["mismatches"] += 1

    return summary


def build_report(
    dataset: dict[str, Any],
    dataset_sha256: str,
) -> dict[str, Any]:
    """Execute all regression cases and build the evidence report."""

    results = [
        evaluate_case(case)
        for case in dataset["cases"]
    ]

    mismatches = [
        result
        for result in results
        if not result["expectation_met"]
    ]

    matched_expectations = len(results) - len(mismatches)

    return {
        "report_id": "deterministic-evaluator-regression-v1-report",
        "evidence_class": "EXPERIMENTAL",
        "dataset": {
            "dataset_id": dataset["dataset_id"],
            "version": dataset["version"],
            "sha256": dataset_sha256,
            "hash_basis": HASH_BASIS,
        },
        "summary": {
            "total_cases": len(results),
            "matched_expectations": matched_expectations,
            "mismatches": len(mismatches),
            "all_expectations_met": not mismatches,
            "by_evaluation_id": build_evaluation_summary(results),
        },
        "results": results,
    }


def write_report(report: dict[str, Any], path: Path) -> None:
    """Write the regression report as stable human-readable JSON."""

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def print_summary(report: dict[str, Any]) -> None:
    """Print a concise deterministic-regression summary."""

    summary = report["summary"]

    print("Deterministic evaluator regression complete")
    print(f"Total cases: {summary['total_cases']}")
    print(
        "Matched expectations: "
        f"{summary['matched_expectations']}"
    )
    print(f"Mismatches: {summary['mismatches']}")
    print(
        "All expectations met: "
        f"{summary['all_expectations_met']}"
    )

    print()

    for evaluation_id, evaluator_summary in sorted(
        summary["by_evaluation_id"].items()
    ):
        print(
            f"{evaluation_id}: "
            f"{evaluator_summary['matched_expectations']}/"
            f"{evaluator_summary['total_cases']} expectations matched"
        )


def main() -> int:
    """Run the deterministic evaluator regression experiment."""

    dataset, dataset_sha256 = load_dataset(DATASET_PATH)
    report = build_report(dataset, dataset_sha256)

    write_report(report, REPORT_PATH)
    print_summary(report)

    if report["summary"]["mismatches"]:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())