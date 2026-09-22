from reliora.telemetry.failures import FailureCategory


def test_failure_categories_match_operational_contract() -> None:
    """NFR-REL-004: runtime failure taxonomy matches the operations contract."""

    assert tuple(category.value for category in FailureCategory) == (
        "VALIDATION",
        "ROUTING",
        "KNOWLEDGE",
        "AUTHORIZATION",
        "MODEL",
        "TOOL",
        "BACKEND",
        "PERSISTENCE",
        "IDEMPOTENCY",
        "TIMEOUT",
        "THROTTLING",
        "SECURITY",
        "TELEMETRY",
        "DEPLOYMENT",
        "UNKNOWN",
    )
