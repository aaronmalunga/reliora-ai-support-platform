"""Validate versioned routing experiment data.

This module contains mechanical integrity checks for the Reliora routing
benchmark. It intentionally validates dataset structure and governance rules;
it does not determine whether a human-assigned intent label is semantically
correct.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROUTING_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROUTING_ROOT / "data"

FAMILY_MANIFEST_PATH = DATA_DIR / "routing-intent-v1-families.json"
DATASET_PATH = DATA_DIR / "routing-intent-v1.json"

ALLOWED_INTENTS = {"BUG", "PLATFORM", "OTHER"}
ALLOWED_VARIANTS = {"A", "B", "C", "D"}
ALLOWED_DATASET_STATUSES = {
    "DESIGN_COMPLETE_PENDING_REVIEW",
    "FROZEN",
}
ALLOWED_MANIFEST_STATUSES = {
    "DESIGN_IN_PROGRESS",
    "FROZEN",
}

EXPECTED_TOTAL_RECORDS = 180
EXPECTED_RECORDS_PER_INTENT = 60

EXPECTED_RECORD_SPLIT_COUNTS = {
    "train": 108,
    "validation": 36,
    "test": 36,
}

EXPECTED_RECORD_INTENT_SPLIT_COUNTS = {
    ("BUG", "train"): 36,
    ("BUG", "validation"): 12,
    ("BUG", "test"): 12,
    ("PLATFORM", "train"): 36,
    ("PLATFORM", "validation"): 12,
    ("PLATFORM", "test"): 12,
    ("OTHER", "train"): 36,
    ("OTHER", "validation"): 12,
    ("OTHER", "test"): 12,
}

REQUIRED_DATASET_RECORD_FIELDS = {
    "case_id",
    "family_id",
    "variant_id",
    "message",
    "expected_intent",
    "split",
    "provenance",
}

ALLOWED_SPLITS = {"train", "validation", "test"}

EXPECTED_TOTAL_FAMILIES = 45
EXPECTED_FAMILIES_PER_INTENT = 15

EXPECTED_SPLIT_COUNTS = {
    "train": 27,
    "validation": 9,
    "test": 9,
}

EXPECTED_INTENT_SPLIT_COUNTS = {
    ("BUG", "train"): 9,
    ("BUG", "validation"): 3,
    ("BUG", "test"): 3,
    ("PLATFORM", "train"): 9,
    ("PLATFORM", "validation"): 3,
    ("PLATFORM", "test"): 3,
    ("OTHER", "train"): 9,
    ("OTHER", "validation"): 3,
    ("OTHER", "test"): 3,
}

REQUIRED_FAMILY_FIELDS = {
    "family_id",
    "intent",
    "split",
    "scenario",
    "label_rationale",
    "stressors",
}


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from disk."""
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
      raise TypeError(f"{path} must contain a top-level JSON object.")

    return payload


def require_non_empty_string(value: Any, field_name: str, family_id: str) -> None:
    """Require a non-empty string value."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"{family_id}: field '{field_name}' must be a non-empty string."
        )


def validate_manifest_metadata(manifest: dict[str, Any]) -> None:
    """Validate top-level family-manifest identity and policy metadata."""
    expected_values = {
        "manifest_id": "routing-intent-v1-families",
        "dataset_id": "routing-intent-v1",
        "version": "1.0.0",
        "provenance": "SYNTHETIC_ASSUMPTION",
    }

    for field_name, expected_value in expected_values.items():
        actual = manifest.get(field_name)
        if actual != expected_value:
            raise ValueError(
                f"Manifest field '{field_name}' must be {expected_value!r}; "
                f"received {actual!r}."
            )

    status = manifest.get("status")
    if status not in ALLOWED_MANIFEST_STATUSES:
        raise ValueError(
            f"Manifest status must be one of "
            f"{sorted(ALLOWED_MANIFEST_STATUSES)}; received {status!r}."
        )

    split_policy = manifest.get("split_policy")
    if not isinstance(split_policy, dict):
        raise TypeError("Manifest 'split_policy' must be a JSON object.")

    expected_policy = {
        "unit": "semantic_family",
        "train_families_per_intent": 9,
        "validation_families_per_intent": 3,
        "test_families_per_intent": 3,
        "variants_per_family": 4,
    }

    for field_name, expected_policy_value in expected_policy.items():
        actual = split_policy.get(field_name)
        if actual != expected_policy_value:
            raise ValueError(
                f"split_policy.{field_name} must be {expected_policy_value!r}; "
                f"received {actual!r}."
            )

def validate_family_record(family: Any, index: int) -> None:
    """Validate one semantic-family record."""
    if not isinstance(family, dict):
        raise TypeError(f"Family at index {index} must be a JSON object.")

    missing_fields = REQUIRED_FAMILY_FIELDS - family.keys()
    if missing_fields:
        raise ValueError(
            f"Family at index {index} is missing required fields: "
            f"{sorted(missing_fields)}."
        )

    family_id = family["family_id"]
    require_non_empty_string(family_id, "family_id", f"index-{index}")

    intent = family["intent"]
    if intent not in ALLOWED_INTENTS:
        raise ValueError(
            f"{family_id}: unsupported intent {intent!r}. "
            f"Allowed intents: {sorted(ALLOWED_INTENTS)}."
        )

    split = family["split"]
    if split not in ALLOWED_SPLITS:
        raise ValueError(
            f"{family_id}: unsupported split {split!r}. "
            f"Allowed splits: {sorted(ALLOWED_SPLITS)}."
        )

    require_non_empty_string(family["scenario"], "scenario", family_id)
    require_non_empty_string(
        family["label_rationale"],
        "label_rationale",
        family_id,
    )

    stressors = family["stressors"]
    if not isinstance(stressors, list) or not stressors:
        raise ValueError(
            f"{family_id}: 'stressors' must be a non-empty list."
        )

    for stressor in stressors:
        require_non_empty_string(stressor, "stressors[]", family_id)


def validate_family_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    """Validate the complete routing semantic-family manifest."""
    validate_manifest_metadata(manifest)

    families = manifest.get("families")
    if not isinstance(families, list):
        raise TypeError("Manifest 'families' must be a JSON array.")

    if len(families) != EXPECTED_TOTAL_FAMILIES:
        raise ValueError(
            f"Expected {EXPECTED_TOTAL_FAMILIES} families; "
            f"received {len(families)}."
        )

    for index, family in enumerate(families):
        validate_family_record(family, index)

    family_ids = [family["family_id"] for family in families]
    duplicate_ids = sorted(
        family_id
        for family_id, count in Counter(family_ids).items()
        if count > 1
    )

    if duplicate_ids:
        raise ValueError(
            f"Duplicate family IDs detected: {duplicate_ids}."
        )

    intent_counts = Counter(family["intent"] for family in families)
    expected_intent_counts = {
        intent: EXPECTED_FAMILIES_PER_INTENT
        for intent in ALLOWED_INTENTS
    }

    if intent_counts != expected_intent_counts:
        raise ValueError(
            "Intent family counts do not match specification. "
            f"Expected {expected_intent_counts}; received {dict(intent_counts)}."
        )

    split_counts = Counter(family["split"] for family in families)
    if split_counts != EXPECTED_SPLIT_COUNTS:
        raise ValueError(
            "Split family counts do not match specification. "
            f"Expected {EXPECTED_SPLIT_COUNTS}; received {dict(split_counts)}."
        )

    intent_split_counts = Counter(
        (family["intent"], family["split"])
        for family in families
    )

    if intent_split_counts != EXPECTED_INTENT_SPLIT_COUNTS:
        raise ValueError(
            "Intent/split family counts do not match specification. "
            f"Expected {EXPECTED_INTENT_SPLIT_COUNTS}; "
            f"received {dict(intent_split_counts)}."
        )

    return {
        "total_families": len(families),
        "intent_counts": dict(sorted(intent_counts.items())),
        "split_counts": dict(sorted(split_counts.items())),
        "duplicate_family_ids": duplicate_ids,
    }


def validate_dataset_metadata(dataset: dict[str, Any]) -> None:
    """Validate top-level routing-dataset identity and metadata."""
    expected_values = {
        "dataset_id": "routing-intent-v1",
        "version": "1.0.0",
        "provenance": "SYNTHETIC_ASSUMPTION",
        "family_manifest_id": "routing-intent-v1-families",
    }

    for field_name, expected_value in expected_values.items():
        actual = dataset.get(field_name)
        if actual != expected_value:
            raise ValueError(
                f"Dataset field '{field_name}' must be {expected_value!r}; "
                f"received {actual!r}."
            )

    status = dataset.get("status")
    if status not in ALLOWED_DATASET_STATUSES:
        raise ValueError(
            f"Dataset status must be one of "
            f"{sorted(ALLOWED_DATASET_STATUSES)}; received {status!r}."
        )

    record_count = dataset.get("record_count")
    if record_count != EXPECTED_TOTAL_RECORDS:
        raise ValueError(
            f"Dataset record_count must be {EXPECTED_TOTAL_RECORDS}; "
            f"received {record_count!r}."
        )


def validate_dataset_record(record: Any, index: int) -> None:
    """Validate the structure of one routing-dataset record."""
    if not isinstance(record, dict):
        raise TypeError(
            f"Dataset record at index {index} must be a JSON object."
        )

    missing_fields = REQUIRED_DATASET_RECORD_FIELDS - record.keys()
    if missing_fields:
        raise ValueError(
            f"Dataset record at index {index} is missing required fields: "
            f"{sorted(missing_fields)}."
        )

    case_id = record["case_id"]
    family_id = record["family_id"]
    variant_id = record["variant_id"]
    message = record["message"]

    require_non_empty_string(case_id, "case_id", f"record-{index}")
    require_non_empty_string(family_id, "family_id", case_id)
    require_non_empty_string(variant_id, "variant_id", case_id)
    require_non_empty_string(message, "message", case_id)

    expected_intent = record["expected_intent"]
    if expected_intent not in ALLOWED_INTENTS:
        raise ValueError(
            f"{case_id}: unsupported expected_intent "
            f"{expected_intent!r}."
        )

    split = record["split"]
    if split not in ALLOWED_SPLITS:
        raise ValueError(
            f"{case_id}: unsupported split {split!r}."
        )

    if variant_id not in ALLOWED_VARIANTS:
        raise ValueError(
            f"{case_id}: unsupported variant_id {variant_id!r}. "
            f"Allowed variants: {sorted(ALLOWED_VARIANTS)}."
        )

    provenance = record["provenance"]
    if provenance != "SYNTHETIC_ASSUMPTION":
        raise ValueError(
            f"{case_id}: provenance must be "
            f"'SYNTHETIC_ASSUMPTION'; received {provenance!r}."
        )


def validate_routing_dataset(
    dataset: dict[str, Any],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    """Validate routing records against the semantic-family manifest."""
    validate_dataset_metadata(dataset)

    records = dataset.get("records")
    if not isinstance(records, list):
        raise TypeError("Dataset 'records' must be a JSON array.")

    if len(records) != EXPECTED_TOTAL_RECORDS:
        raise ValueError(
            f"Expected {EXPECTED_TOTAL_RECORDS} dataset records; "
            f"received {len(records)}."
        )

    for index, record in enumerate(records):
        validate_dataset_record(record, index)

    families = manifest.get("families")
    if not isinstance(families, list):
        raise TypeError("Manifest 'families' must be a JSON array.")

    manifest_index = {
        family["family_id"]: family
        for family in families
    }

    case_ids = [record["case_id"] for record in records]
    duplicate_case_ids = sorted(
        case_id
        for case_id, count in Counter(case_ids).items()
        if count > 1
    )

    if duplicate_case_ids:
        raise ValueError(
            f"Duplicate dataset case IDs detected: {duplicate_case_ids}."
        )

    normalized_messages = [
        record["message"].strip().casefold()
        for record in records
    ]

    duplicate_messages = sorted(
        message
        for message, count in Counter(normalized_messages).items()
        if count > 1
    )

    if duplicate_messages:
        raise ValueError(
            "Exact duplicate customer messages detected after "
            f"case/whitespace normalization: {duplicate_messages}."
        )

    records_by_family: dict[str, list[dict[str, Any]]] = {}

    for record in records:
        case_id = record["case_id"]
        family_id = record["family_id"]

        if family_id not in manifest_index:
            raise ValueError(
                f"{case_id}: unknown family_id {family_id!r}."
            )

        family = manifest_index[family_id]

        if record["expected_intent"] != family["intent"]:
            raise ValueError(
                f"{case_id}: expected_intent "
                f"{record['expected_intent']!r} does not match "
                f"manifest intent {family['intent']!r}."
            )

        if record["split"] != family["split"]:
            raise ValueError(
                f"{case_id}: split {record['split']!r} does not "
                f"match manifest split {family['split']!r}."
            )

        records_by_family.setdefault(family_id, []).append(record)

    dataset_family_ids = set(records_by_family)
    manifest_family_ids = set(manifest_index)

    if dataset_family_ids != manifest_family_ids:
        missing_families = sorted(
            manifest_family_ids - dataset_family_ids
        )
        unexpected_families = sorted(
            dataset_family_ids - manifest_family_ids
        )

        raise ValueError(
            "Dataset family coverage does not match manifest. "
            f"Missing: {missing_families}; "
            f"unexpected: {unexpected_families}."
        )

    for family_id, family_records in records_by_family.items():
        if len(family_records) != 4:
            raise ValueError(
                f"{family_id}: expected exactly 4 records; "
                f"received {len(family_records)}."
            )

        variants = {
            record["variant_id"]
            for record in family_records
        }

        if variants != ALLOWED_VARIANTS:
            raise ValueError(
                f"{family_id}: variants must be "
                f"{sorted(ALLOWED_VARIANTS)}; "
                f"received {sorted(variants)}."
            )

    intent_counts = Counter(
        record["expected_intent"]
        for record in records
    )

    expected_intent_counts = {
        intent: EXPECTED_RECORDS_PER_INTENT
        for intent in ALLOWED_INTENTS
    }

    if intent_counts != expected_intent_counts:
        raise ValueError(
            "Dataset intent counts do not match specification. "
            f"Expected {expected_intent_counts}; "
            f"received {dict(intent_counts)}."
        )

    split_counts = Counter(
        record["split"]
        for record in records
    )

    if split_counts != EXPECTED_RECORD_SPLIT_COUNTS:
        raise ValueError(
            "Dataset split counts do not match specification. "
            f"Expected {EXPECTED_RECORD_SPLIT_COUNTS}; "
            f"received {dict(split_counts)}."
        )

    intent_split_counts = Counter(
        (record["expected_intent"], record["split"])
        for record in records
    )

    if intent_split_counts != EXPECTED_RECORD_INTENT_SPLIT_COUNTS:
        raise ValueError(
            "Dataset intent/split counts do not match specification. "
            f"Expected {EXPECTED_RECORD_INTENT_SPLIT_COUNTS}; "
            f"received {dict(intent_split_counts)}."
        )

    return {
        "total_records": len(records),
        "total_families": len(records_by_family),
        "intent_counts": dict(sorted(intent_counts.items())),
        "split_counts": dict(sorted(split_counts.items())),
        "duplicate_case_ids": duplicate_case_ids,
        "duplicate_messages": duplicate_messages,
    }


def main() -> int:
    """Run routing-data validation and return a process exit code."""
    try:
        manifest = load_json(FAMILY_MANIFEST_PATH)
        manifest_summary = validate_family_manifest(manifest)

        dataset = load_json(DATASET_PATH)
        dataset_summary = validate_routing_dataset(dataset, manifest)

    except (
        OSError,
        json.JSONDecodeError,
        TypeError,
        ValueError,
    ) as exc:
        print("Routing data validation FAILED")
        print(f"Reason: {exc}")
        return 1

    print("Routing data validation PASSED")

    print()
    print("Family manifest:")
    print(f"  File: {FAMILY_MANIFEST_PATH.name}")
    print(f"  Total families: {manifest_summary['total_families']}")

    print("  Intent counts:")
    for intent, count in manifest_summary["intent_counts"].items():
        print(f"    {intent}: {count}")

    print("  Split counts:")
    for split, count in manifest_summary["split_counts"].items():
        print(f"    {split}: {count}")

    print("  Duplicate family IDs: 0")

    print()
    print("Routing dataset:")
    print(f"  File: {DATASET_PATH.name}")
    print(f"  Total records: {dataset_summary['total_records']}")
    print(f"  Total families: {dataset_summary['total_families']}")

    print("  Intent counts:")
    for intent, count in dataset_summary["intent_counts"].items():
        print(f"    {intent}: {count}")

    print("  Split counts:")
    for split, count in dataset_summary["split_counts"].items():
        print(f"    {split}: {count}")

    print("  Duplicate case IDs: 0")
    print("  Exact duplicate messages: 0")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
