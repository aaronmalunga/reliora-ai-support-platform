"""Measure local synthetic concurrency behaviour of the Reliora ticket runtime.

This experiment measures the in-process LambdaBugReportRuntime application path.
It does not measure AWS Lambda, Gateway, DynamoDB, AgentCore, network behaviour,
AWS throttling, cold starts, or cloud cost.
"""

from __future__ import annotations

import json
import os
import platform
import statistics
import subprocess
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter_ns
from uuid import NAMESPACE_URL, UUID, uuid5

import pydantic

from reliora.adapters.aws.gateway_bug_report_operation import (
    TrustedOperationIdentity,
)
from reliora.adapters.aws.lambda_bug_report_runtime import (
    LambdaBugReportRuntime,
)
from reliora.domain.operations import BugReportOperation
from reliora.domain.tickets import TicketCreationConfirmation
from reliora.services.ticket_execution import (
    TicketExecutionResult,
    TicketExecutionStatus,
)

PERFORMANCE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PERFORMANCE_ROOT.parents[1]

RESULT_PATH = (
    PERFORMANCE_ROOT
    / "results"
    / "local-ticket-runtime-v1.json"
)

EXPERIMENT_ID = "local-ticket-runtime-v1"
EVIDENCE_CLASSIFICATION = "EXPERIMENTAL"
WORKLOAD_PROVENANCE = "SYNTHETIC_PERFORMANCE_PROBE"

CONCURRENCY_LEVELS = (
    1,
    2,
    4,
    8,
)

REQUESTS_PER_LEVEL = 25_000
WARMUP_REQUESTS = 25

CONFIRMED_AT = datetime(
    2026,
    9,
    8,
    12,
    0,
    tzinfo=UTC,
)

SESSION_ID = uuid5(
    NAMESPACE_URL,
    "reliora:performance:local-ticket-runtime-v1:session",
)


@dataclass(frozen=True, slots=True)
class SyntheticLambdaContext:
    """Deterministic local stand-in for invocation-owned Lambda context."""

    request_index: int


class SyntheticIdentityResolver:
    """Resolve deterministic trusted identities from synthetic context."""

    def resolve(
        self,
        context: object,
    ) -> TrustedOperationIdentity:
        if not isinstance(
            context,
            SyntheticLambdaContext,
        ):
            raise TypeError(
                "Synthetic performance measurement requires "
                "SyntheticLambdaContext."
            )

        return TrustedOperationIdentity(
            operation_id=synthetic_uuid(
                "operation",
                context.request_index,
            ),
            request_id=synthetic_uuid(
                "request",
                context.request_index,
            ),
            session_id=SESSION_ID,
        )


class SyntheticTicketExecution:
    """Deterministic side-effect double for local performance measurement."""

    def execute(
        self,
        operation: BugReportOperation,
    ) -> TicketExecutionResult:
        ticket_id = (
            "SYN-"
            f"{operation.operation_id.hex[:12].upper()}"
        )

        return TicketExecutionResult(
            operation_id=operation.operation_id,
            request_id=operation.request_id,
            status=TicketExecutionStatus.CREATED,
            confirmation=TicketCreationConfirmation(
                operation_id=operation.operation_id,
                ticket_id=ticket_id,
                provider="synthetic-performance-double",
                confirmed_at=CONFIRMED_AT,
            ),
        )


@dataclass(frozen=True, slots=True)
class RequestObservation:
    """Measured result of one local synthetic runtime invocation."""

    latency_ms: float
    success: bool
    failure_class: str | None


@dataclass(frozen=True, slots=True)
class ConcurrencySummary:
    """Summary of one requested local concurrency level."""

    requested_concurrency: int
    request_count: int
    successful_requests: int
    failed_requests: int
    elapsed_seconds: float
    throughput_requests_per_second: float
    mean_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    failure_classes: tuple[tuple[str, int], ...]


def synthetic_uuid(
    identity_kind: str,
    request_index: int,
) -> UUID:
    """Return deterministic synthetic identity for one measured request."""

    return uuid5(
        NAMESPACE_URL,
        (
            "reliora:performance:"
            f"{EXPERIMENT_ID}:"
            f"{identity_kind}:"
            f"{request_index}"
        ),
    )


def synthetic_event() -> dict[str, object]:
    """Return one clearly synthetic complete bug-report event."""

    return {
        "description": (
            "Synthetic checkout failure used for local performance testing."
        ),
        "stepsToReproduce": (
            "Open synthetic checkout and select synthetic Pay."
        ),
        "environment": (
            "Synthetic browser on synthetic operating system."
        ),
    }


def build_synthetic_runtime() -> LambdaBugReportRuntime:
    """Compose the real local runtime around deterministic test doubles."""

    return LambdaBugReportRuntime(
        ticket_execution=SyntheticTicketExecution(),
        identity_resolver=SyntheticIdentityResolver(),
    )


def percentile(
    values: list[float],
    probability: float,
) -> float:
    """Return a linearly interpolated percentile."""

    if not values:
        raise ValueError(
            "Cannot calculate a percentile from no values."
        )

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


def invoke_once(
    runtime: LambdaBugReportRuntime,
    request_index: int,
) -> RequestObservation:
    """Measure one in-process runtime invocation."""

    started_ns = perf_counter_ns()

    try:
        response = runtime.handle(
            synthetic_event(),
            SyntheticLambdaContext(
                request_index=request_index,
            ),
        )
    except Exception as exc:  # noqa: BLE001
        finished_ns = perf_counter_ns()

        return RequestObservation(
            latency_ms=(
                finished_ns - started_ns
            )
            / 1_000_000,
            success=False,
            failure_class=type(exc).__name__,
        )

    finished_ns = perf_counter_ns()

    success = (
        response.get("status") == "OPEN"
        and response.get("executionStatus") == "CREATED"
        and isinstance(
            response.get("ticketId"),
            str,
        )
    )

    return RequestObservation(
        latency_ms=(
            finished_ns - started_ns
        )
        / 1_000_000,
        success=success,
        failure_class=(
            None
            if success
            else "UNEXPECTED_RESPONSE"
        ),
    )


def warm_up(
    runtime: LambdaBugReportRuntime,
    request_count: int,
) -> None:
    """Perform sequential warm-up calls outside measured results."""

    if request_count < 0:
        raise ValueError(
            "Warm-up request count cannot be negative."
        )

    for offset in range(
        request_count
    ):
        observation = invoke_once(
            runtime,
            -(offset + 1),
        )

        if not observation.success:
            raise RuntimeError(
                "Synthetic warm-up invocation failed: "
                f"{observation.failure_class}."
            )


def measure_concurrency(
    runtime: LambdaBugReportRuntime,
    *,
    requested_concurrency: int,
    request_count: int,
    start_index: int,
) -> ConcurrencySummary:
    """Measure one local synthetic concurrency probe."""

    if requested_concurrency < 1:
        raise ValueError(
            "Requested concurrency must be at least 1."
        )

    if request_count < 1:
        raise ValueError(
            "Measured request count must be at least 1."
        )

    if start_index < 0:
        raise ValueError(
            "Measured request index cannot be negative."
        )

    started_ns = perf_counter_ns()

    with ThreadPoolExecutor(
        max_workers=requested_concurrency
    ) as executor:
        futures = [
            executor.submit(
                invoke_once,
                runtime,
                request_index,
            )
            for request_index in range(
                start_index,
                start_index + request_count,
            )
        ]

        observations = [
            future.result()
            for future in futures
        ]

    finished_ns = perf_counter_ns()

    elapsed_seconds = (
        finished_ns - started_ns
    ) / 1_000_000_000

    if elapsed_seconds <= 0.0:
        raise RuntimeError(
            "Measured elapsed time must be greater than zero."
        )

    latencies = [
        observation.latency_ms
        for observation in observations
    ]

    successful_requests = sum(
        observation.success
        for observation in observations
    )

    failed_requests = (
        request_count
        - successful_requests
    )

    failure_counts = Counter(
        observation.failure_class
        for observation in observations
        if observation.failure_class is not None
    )

    return ConcurrencySummary(
        requested_concurrency=requested_concurrency,
        request_count=request_count,
        successful_requests=successful_requests,
        failed_requests=failed_requests,
        elapsed_seconds=elapsed_seconds,
        throughput_requests_per_second=(
            request_count / elapsed_seconds
        ),
        mean_latency_ms=statistics.fmean(
            latencies
        ),
        p50_latency_ms=percentile(
            latencies,
            0.50,
        ),
        p95_latency_ms=percentile(
            latencies,
            0.95,
        ),
        p99_latency_ms=percentile(
            latencies,
            0.99,
        ),
        failure_classes=tuple(
            sorted(
                failure_counts.items()
            )
        ),
    )


def concurrency_summary_to_dict(
    summary: ConcurrencySummary,
) -> dict[str, object]:
    """Serialize one concurrency result into JSON-ready evidence."""

    return {
        "requested_concurrency": summary.requested_concurrency,
        "request_count": summary.request_count,
        "successful_requests": summary.successful_requests,
        "failed_requests": summary.failed_requests,
        "elapsed_seconds": summary.elapsed_seconds,
        "throughput_requests_per_second": (
            summary.throughput_requests_per_second
        ),
        "mean_latency_ms": summary.mean_latency_ms,
        "p50_latency_ms": summary.p50_latency_ms,
        "p95_latency_ms": summary.p95_latency_ms,
        "p99_latency_ms": summary.p99_latency_ms,
        "failure_classes": {
            name: count
            for name, count
            in summary.failure_classes
        },
    }


def git_revision() -> str:
    """Return repository Git revision used for the experiment."""

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


def run_local_baseline(
    *,
    concurrency_levels: tuple[int, ...] = CONCURRENCY_LEVELS,
    requests_per_level: int = REQUESTS_PER_LEVEL,
    warmup_requests: int = WARMUP_REQUESTS,
) -> dict[str, object]:
    """Run the local synthetic ticket-runtime performance baseline."""

    if not concurrency_levels:
        raise ValueError(
            "At least one concurrency level is required."
        )

    if any(
        level < 1
        for level in concurrency_levels
    ):
        raise ValueError(
            "All concurrency levels must be at least 1."
        )

    if len(
        set(concurrency_levels)
    ) != len(concurrency_levels):
        raise ValueError(
            "Concurrency levels must not contain duplicates."
        )

    if requests_per_level < 1:
        raise ValueError(
            "Requests per level must be at least 1."
        )

    runtime = build_synthetic_runtime()

    warm_up(
        runtime,
        warmup_requests,
    )

    results: list[dict[str, object]] = []
    start_index = 0

    for concurrency in concurrency_levels:
        summary = measure_concurrency(
            runtime,
            requested_concurrency=concurrency,
            request_count=requests_per_level,
            start_index=start_index,
        )

        results.append(
            concurrency_summary_to_dict(
                summary
            )
        )

        start_index += requests_per_level

    return {
        "experiment_id": EXPERIMENT_ID,
        "evidence_classification": EVIDENCE_CLASSIFICATION,
        "experiment_timestamp_utc": datetime.now(
            UTC
        ).isoformat(),
        "benchmark_git_revision": git_revision(),
        "environment": {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "python_implementation": (
                platform.python_implementation()
            ),
            "pydantic_version": pydantic.__version__,
            "logical_cpu_count": os.cpu_count(),
            "timer": "time.perf_counter_ns",
        },
        "measurement_protocol": {
            "workload_provenance": WORKLOAD_PROVENANCE,
            "execution_scope": (
                "local in-process "
                "LambdaBugReportRuntime.handle"
            ),
            "concurrency_levels": list(
                concurrency_levels
            ),
            "requests_per_level": requests_per_level,
            "warmup_requests": warmup_requests,
            "warmup_scope": "sequential local invocations",
            "latency_scope": (
                "runtime.handle execution time inside each worker; "
                "executor queue wait is excluded"
            ),
            "throughput_scope": (
                "wall-clock time from local workload submission "
                "through completion"
            ),
            "capacity_target_status": "NOT_ESTABLISHED",
            "interpretation": (
                "Probe levels are experimental inputs, not "
                "production concurrency targets."
            ),
            "excluded_from_evidence": [
                "AWS Lambda infrastructure",
                "Lambda cold starts",
                "Lambda service scheduling and scaling",
                "Amazon Bedrock AgentCore",
                "AgentCore Gateway service and network overhead",
                "DynamoDB network and service latency",
                "AWS service throttling",
                "AWS billing and cloud cost",
                "internet and external network latency",
            ],
        },
        "total_measured_requests": (
            len(concurrency_levels)
            * requests_per_level
        ),
        "results": results,
    }


def write_report(
    report: dict[str, object],
    path: Path = RESULT_PATH,
) -> None:
    """Write experiment evidence as deterministic formatted JSON."""

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
    """Run the local synthetic baseline and write evidence."""

    try:
        report = run_local_baseline()
        write_report(report)
    except (
        OSError,
        RuntimeError,
        subprocess.CalledProcessError,
        TypeError,
        ValueError,
    ) as exc:
        print(
            "Local ticket-runtime performance measurement FAILED"
        )
        print(
            f"Reason: {exc}"
        )
        return 1

    print(
        "Local ticket-runtime performance measurement completed"
    )
    print(
        f"Experiment: {EXPERIMENT_ID}"
    )
    print(
        f"Evidence: {EVIDENCE_CLASSIFICATION}"
    )
    print(
        "Capacity target status: NOT_ESTABLISHED"
    )
    print(
        f"Measured requests: {report['total_measured_requests']}"
    )
    print(
        f"Report: {RESULT_PATH}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
