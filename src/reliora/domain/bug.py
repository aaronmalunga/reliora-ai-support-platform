"""Domain contracts for Reliora bug-report collection."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, field_validator


class BugField(StrEnum):
    """Required fields in the Reliora bug-report workflow."""

    DESCRIPTION = "description"
    STEPS_TO_REPRODUCE = "steps_to_reproduce"
    ENVIRONMENT = "environment"


class BugReportDraft(BaseModel):
    """Validated state collected before a bug ticket may be authorized."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    description: str | None = None
    steps_to_reproduce: str | None = None
    environment: str | None = None

    @field_validator(
        "description",
        "steps_to_reproduce",
        "environment",
        mode="before",
    )
    @classmethod
    def normalize_optional_text(cls, value: object) -> object:
        """Normalize blank bug-field input to an uncollected value."""

        if isinstance(value, str):
            normalized = value.strip()
            return normalized or None

        return value

    @property
    def missing_fields(self) -> tuple[BugField, ...]:
        """Return required fields that have not yet been collected."""

        missing: list[BugField] = []

        if self.description is None:
            missing.append(BugField.DESCRIPTION)

        if self.steps_to_reproduce is None:
            missing.append(BugField.STEPS_TO_REPRODUCE)

        if self.environment is None:
            missing.append(BugField.ENVIRONMENT)

        return tuple(missing)

    @property
    def is_complete(self) -> bool:
        """Return whether all FR-007 fields are present."""

        return not self.missing_fields

    @property
    def next_missing_field(self) -> BugField | None:
        """Return one missing field for incremental collection."""

        if not self.missing_fields:
            return None

        return self.missing_fields[0]