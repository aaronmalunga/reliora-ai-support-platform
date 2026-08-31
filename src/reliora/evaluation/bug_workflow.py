"""Deterministic evaluation of bug-report workflow behaviour."""

from collections.abc import Iterable
from enum import StrEnum

from reliora.evaluation.models import EvaluationFinding


class BugField(StrEnum):
    """Required fields in the Reliora bug-report workflow."""

    DESCRIPTION = "description"
    STEPS_TO_REPRODUCE = "steps_to_reproduce"
    ENVIRONMENT = "environment"


def evaluate_incremental_bug_collection(
    *,
    missing_fields: Iterable[BugField],
    requested_fields: Iterable[BugField],
) -> EvaluationFinding:
    """Evaluate INV-004: request at most one required missing field per turn."""

    missing = tuple(dict.fromkeys(missing_fields))
    requested = tuple(dict.fromkeys(requested_fields))

    invalid_requested_fields = tuple(
        field for field in requested if field not in missing
    )

    if not missing:
        passed = not requested
    else:
        passed = len(requested) == 1 and not invalid_requested_fields

    if passed:
        message = "Bug-field collection satisfies the incremental collection policy."
    elif len(requested) > 1:
        message = "More than one required bug field was requested in a single turn."
    elif invalid_requested_fields:
        message = "The workflow requested a field that was not currently missing."
    else:
        message = "The workflow did not request exactly one required missing field."

    return EvaluationFinding(
        evaluation_id="INV-004",
        passed=passed,
        message=message,
        evidence={
            "missing_fields": [field.value for field in missing],
            "requested_fields": [field.value for field in requested],
            "invalid_requested_fields": [
                field.value for field in invalid_requested_fields
            ],
        },
    )