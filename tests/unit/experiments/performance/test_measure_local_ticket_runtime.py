"""Unit tests for local ticket-runtime performance measurement."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import experiments.performance.scripts.measure_local_ticket_runtime as performance


def test_percentile_returns_expected_interpolated_values() -> None:
    values = [
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
    ]

    assert performance.percentile(
        values,
        0.0,
    ) == pytest.approx(1.0)

    assert performance.percentile(
        values,
        0.5,
    ) == pytest.approx(3.0)

    assert performance.percentile(
        values,
        0.95,
    ) == pytest.approx(4.8)

    assert performance.percentile(
        values,
        1.0,
    ) == pytest.approx(5.0)


def test_percentile_rejects_invalid_inputs() -> None:
    with pytest.raises(
        ValueError,
        match="no values",
    ):
        performance.percentile(
            [],
            0.5,
        )

    with pytest.raises(
        ValueError,
        match="between 0.0 and 1.0",
    ):
        performance.percentile(
            [1.0],
            1.1,
        )


def test_measure_concurrency_records_requested_workload() -> None:
    runtime = performance.build_synthetic_runtime()

    summary = performance.measure_concurrency(
        runtime,
        requested_concurrency=2,
        request_count=8,
        start_index=0,
    )

    assert summary.requested_concurrency == 2
    assert summary.request_count == 8
    assert summary.successful_requests == 8
    assert summary.failed_requests == 0
    assert summary.failure_classes == ()

    assert summary.elapsed_seconds > 0.0
    assert summary.throughput_requests_per_second > 0.0

    assert summary.mean_latency_ms >= 0.0
    assert summary.p50_latency_ms >= 0.0
    assert summary.p95_latency_ms >= 0.0
    assert summary.p99_latency_ms >= 0.0


@pytest.mark.parametrize(
    (
        "requested_concurrency",
        "request_count",
        "start_index",
        "expected_message",
    ),
    [
        (
            0,
            1,
            0,
            "at least 1",
        ),
        (
            1,
            0,
            0,
            "at least 1",
        ),
        (
            1,
            1,
            -1,
            "cannot be negative",
        ),
    ],
)
def test_measure_concurrency_rejects_invalid_workload(
    requested_concurrency: int,
    request_count: int,
    start_index: int,
    expected_message: str,
) -> None:
    runtime = performance.build_synthetic_runtime()

    with pytest.raises(
        ValueError,
        match=expected_message,
    ):
        performance.measure_concurrency(
            runtime,
            requested_concurrency=requested_concurrency,
            request_count=request_count,
            start_index=start_index,
        )


def test_warm_up_rejects_negative_request_count() -> None:
    runtime = performance.build_synthetic_runtime()

    with pytest.raises(
        ValueError,
        match="cannot be negative",
    ):
        performance.warm_up(
            runtime,
            -1,
        )


def test_local_baseline_reports_synthetic_scope(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        performance,
        "git_revision",
        lambda: "synthetic-git-revision",
    )

    report = performance.run_local_baseline(
        concurrency_levels=(
            1,
            2,
        ),
        requests_per_level=4,
        warmup_requests=2,
    )

    assert report["experiment_id"] == (
        "local-ticket-runtime-v1"
    )
    assert report["evidence_classification"] == (
        "EXPERIMENTAL"
    )
    assert report["benchmark_git_revision"] == (
        "synthetic-git-revision"
    )
    assert report["total_measured_requests"] == 8

    protocol = report["measurement_protocol"]

    assert isinstance(
        protocol,
        dict,
    )

    assert protocol["workload_provenance"] == (
        "SYNTHETIC_PERFORMANCE_PROBE"
    )
    assert protocol["capacity_target_status"] == (
        "NOT_ESTABLISHED"
    )
    assert protocol["concurrency_levels"] == [
        1,
        2,
    ]

    exclusions = protocol["excluded_from_evidence"]

    assert isinstance(
        exclusions,
        list,
    )

    assert "AWS Lambda infrastructure" in exclusions
    assert "AWS billing and cloud cost" in exclusions

    results = report["results"]

    assert isinstance(
        results,
        list,
    )
    assert len(results) == 2

    assert [
        result["requested_concurrency"]
        for result in results
    ] == [
        1,
        2,
    ]

    assert all(
        result["failed_requests"] == 0
        for result in results
    )


def test_local_baseline_rejects_duplicate_concurrency_levels() -> None:
    with pytest.raises(
        ValueError,
        match="must not contain duplicates",
    ):
        performance.run_local_baseline(
            concurrency_levels=(
                1,
                1,
            ),
            requests_per_level=2,
            warmup_requests=0,
        )


def test_write_report_creates_json_with_final_newline(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "performance.json"

    report: dict[str, object] = {
        "experiment_id": "synthetic-performance-test",
        "evidence_classification": "EXPERIMENTAL",
    }

    performance.write_report(
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
