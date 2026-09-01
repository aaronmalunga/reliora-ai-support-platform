"""Load frozen data for the Reliora routing benchmark.

This module provides the shared data boundary used by routing benchmark
candidates.

Dataset metadata remains available for audit and evidence purposes, but model
candidates should consume only the customer message as a predictive feature.
Fields such as case ID, family ID, variant ID, split, and provenance must not
be used as model features.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast

Intent = Literal["BUG", "PLATFORM", "OTHER"]
Split = Literal["train", "validation", "test"]

ROUTING_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROUTING_ROOT / "data" / "routing-intent-v1.json"

EXPECTED_DATASET_ID = "routing-intent-v1"
EXPECTED_DATASET_VERSION = "1.0.0"
EXPECTED_DATASET_STATUS = "FROZEN"
EXPECTED_RECORD_COUNT = 180

ALLOWED_INTENTS = frozenset({"BUG", "PLATFORM", "OTHER"})
ALLOWED_SPLITS = frozenset({"train", "validation", "test"})


@dataclass(frozen=True, slots=True)
class RoutingRecord:
    """One complete frozen routing benchmark record."""

    case_id: str
    family_id: str
    variant_id: str
    message: str
    expected_intent: Intent
    split: Split
    provenance: str


@dataclass(frozen=True, slots=True)
class ModelExample:
    """Predictive input and supervised target exposed to a candidate."""

    message: str
    expected_intent: Intent


def _require_string(
    record: dict[str, object],
    field_name: str,
    record_index: int,
) -> str:
    """Return a required non-empty string field."""

    value = record.get(field_name)

    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"Record {record_index}: field {field_name!r} "
            "must be a non-empty string."
        )

    return value


def load_routing_records(
    path: Path = DATASET_PATH,
) -> tuple[RoutingRecord, ...]:
    """Load and minimally validate the frozen routing benchmark dataset."""

    payload = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(payload, dict):
        raise TypeError("Routing dataset must contain a top-level JSON object.")

    expected_metadata = {
        "dataset_id": EXPECTED_DATASET_ID,
        "version": EXPECTED_DATASET_VERSION,
        "status": EXPECTED_DATASET_STATUS,
        "record_count": EXPECTED_RECORD_COUNT,
    }

    for field_name, expected_value in expected_metadata.items():
        actual_value = payload.get(field_name)

        if actual_value != expected_value:
            raise ValueError(
                f"Dataset field {field_name!r} must be "
                f"{expected_value!r}; received {actual_value!r}."
            )

    raw_records = payload.get("records")

    if not isinstance(raw_records, list):
        raise TypeError("Dataset field 'records' must contain a JSON array.")

    if len(raw_records) != EXPECTED_RECORD_COUNT:
        raise ValueError(
            "Dataset record count does not match the frozen v1 contract: "
            f"expected {EXPECTED_RECORD_COUNT}, received {len(raw_records)}."
        )

    records: list[RoutingRecord] = []

    for record_index, raw_record in enumerate(raw_records):
        if not isinstance(raw_record, dict):
            raise TypeError(
                f"Record {record_index} must contain a JSON object."
            )

        case_id = _require_string(raw_record, "case_id", record_index)
        family_id = _require_string(raw_record, "family_id", record_index)
        variant_id = _require_string(raw_record, "variant_id", record_index)
        message = _require_string(raw_record, "message", record_index)
        intent_value = _require_string(
            raw_record,
            "expected_intent",
            record_index,
        )
        split_value = _require_string(raw_record, "split", record_index)
        provenance = _require_string(
            raw_record,
            "provenance",
            record_index,
        )

        if intent_value not in ALLOWED_INTENTS:
            raise ValueError(
                f"Record {record_index}: unsupported intent "
                f"{intent_value!r}."
            )

        if split_value not in ALLOWED_SPLITS:
            raise ValueError(
                f"Record {record_index}: unsupported split "
                f"{split_value!r}."
            )

        records.append(
            RoutingRecord(
                case_id=case_id,
                family_id=family_id,
                variant_id=variant_id,
                message=message,
                expected_intent=cast(Intent, intent_value),
                split=cast(Split, split_value),
                provenance=provenance,
            )
        )

    return tuple(records)


def records_for_split(
    records: tuple[RoutingRecord, ...],
    split: Split,
) -> tuple[RoutingRecord, ...]:
    """Return benchmark records assigned to one frozen split."""

    return tuple(record for record in records if record.split == split)


def model_examples_for_split(
    records: tuple[RoutingRecord, ...],
    split: Split,
) -> tuple[ModelExample, ...]:
    """Expose only message text and target labels to benchmark candidates."""

    return tuple(
        ModelExample(
            message=record.message,
            expected_intent=record.expected_intent,
        )
        for record in records_for_split(records, split)
    )
