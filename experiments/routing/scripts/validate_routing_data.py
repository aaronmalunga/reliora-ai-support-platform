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

ALLOWED_INTENTS = {"BUG", "PLATFORM", "OTHER"}
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


def main() -> int:
    """Run routing-data validation and return a process exit code."""
    try:
        manifest = load_json(FAMILY_MANIFEST_PATH)
        summary = validate_family_manifest(manifest)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print("Routing data validation FAILED")
        print(f"Reason: {exc}")
        return 1

    print("Routing data validation PASSED")
    print(f"Manifest: {FAMILY_MANIFEST_PATH.name}")
    print(f"Total families: {summary['total_families']}")

    print("Intent counts:")
    for intent, count in summary["intent_counts"].items():
        print(f"  {intent}: {count}")

    print("Split counts:")
    for split, count in summary["split_counts"].items():
        print(f"  {split}: {count}")

    print("Duplicate family IDs: 0")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())