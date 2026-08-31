"""Run the frozen Stage-1 reproduction dataset through Reliora evaluators."""

import hashlib
import json
from pathlib import Path
from typing import Any

from reliora.evaluation.reproduction import evaluate_reproduction_case

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "evals"
    / "datasets"
    / "stage1-reproduction-v1.json"
)

REPORT_PATH = (
    PROJECT_ROOT
    / "evidence"
    / "generated"
    / "stage1-reproduction-v1-report.json"
)
def normalize_text_bytes_for_hashing(raw_bytes: bytes) -> bytes:
    """Normalize UTF-8 text to LF line endings before hashing."""

    text = raw_bytes.decode("utf-8")
    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")

    return normalized_text.encode("utf-8")

def load_dataset(path: Path) -> tuple[dict[str, Any], str]:
    """Load the reproduction dataset and return it with its SHA-256 hash."""

    raw_bytes = path.read_bytes()
    canonical_bytes = normalize_text_bytes_for_hashing(raw_bytes)

    dataset_sha256 = hashlib.sha256(canonical_bytes).hexdigest()
    dataset = json.loads(canonical_bytes.decode("utf-8"))

    return dataset, dataset_sha256


def build_report(
    dataset: dict[str, Any],
    dataset_sha256: str,
) -> dict[str, Any]:
    """Execute all cases and build a deterministic reproduction report."""

    results = [
        evaluate_reproduction_case(case)
        for case in dataset["cases"]
    ]

    executable_results = [
        result for result in results if result["executed"]
    ]

    documented_results = [
        result for result in results if not result["executed"]
    ]

    mismatches = [
        result
        for result in executable_results
        if result["expectation_met"] is not True
    ]

    detected_defects = [
        result
        for result in executable_results
        if result["status"] == "DETECTED"
    ]

    return {
        "report_id": "stage1-reproduction-v1-report",
        "evidence_class": "EXPERIMENTAL",
        "dataset": {
        "dataset_id": dataset["dataset_id"],
        "version": dataset["version"],
        "sha256": dataset_sha256,
        "hash_basis": "UTF-8 text normalized to LF line endings before SHA-256",
            "source_repository": dataset["source_repository"],
            "source_commit": dataset["source_commit"],
        },
        "summary": {
            "total_cases": len(results),
            "executable_cases": len(executable_results),
            "documented_non_executable_cases": len(documented_results),
            "detected_known_defects": len(detected_defects),
            "mismatches": len(mismatches),
            "all_executable_expectations_met": not mismatches,
        },
        "results": results,
    }


def write_report(report: dict[str, Any], path: Path) -> None:
    """Write the reproduction report as stable, human-readable JSON."""

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
    """Print a concise reproduction summary."""

    summary = report["summary"]

    print("Stage-1 reproduction complete")
    print(f"Total cases: {summary['total_cases']}")
    print(f"Executable cases: {summary['executable_cases']}")
    print(
        "Documented non-executable cases: "
        f"{summary['documented_non_executable_cases']}"
    )
    print(
        "Detected known defects: "
        f"{summary['detected_known_defects']}"
    )
    print(f"Mismatches: {summary['mismatches']}")
    print(
        "All executable expectations met: "
        f"{summary['all_executable_expectations_met']}"
    )


def main() -> int:
    """Run the frozen Stage-1 reproduction experiment."""

    dataset, dataset_sha256 = load_dataset(DATASET_PATH)
    report = build_report(dataset, dataset_sha256)

    write_report(report, REPORT_PATH)
    print_summary(report)

    if report["summary"]["mismatches"]:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())