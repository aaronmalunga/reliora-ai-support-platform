"""Audit semantic quality signals in the Reliora routing dataset.

The structural validator answers whether routing data satisfies hard dataset
contracts. This audit instead surfaces potential quality risks for human
review, including cross-split near-duplicates and strongly class-associated
vocabulary.

Audit findings are diagnostic. A flagged case is not automatically defective.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

ROUTING_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROUTING_ROOT / "data" / "routing-intent-v1.json"
RESULT_PATH = ROUTING_ROOT / "results" / "routing-intent-v1-audit.json"

TOKEN_PATTERN = re.compile(r"[a-z0-9']+")

CROSS_SPLIT_JACCARD_THRESHOLD = 0.55
CROSS_SPLIT_SEQUENCE_THRESHOLD = 0.78

MIN_TOKEN_DOCUMENT_FREQUENCY = 4
TOKEN_LABEL_PURITY_THRESHOLD = 0.80

STOPWORDS = {
    "a",
    "about",
    "after",
    "all",
    "am",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "but",
    "can",
    "do",
    "does",
    "for",
    "from",
    "get",
    "give",
    "how",
    "i",
    "if",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "please",
    "should",
    "that",
    "the",
    "this",
    "to",
    "what",
    "when",
    "where",
    "why",
    "with",
    "you",
    "your",
}

BOUNDARY_TERMS = {
    "account",
    "address",
    "app",
    "checkout",
    "discount",
    "error",
    "order",
    "payment",
    "product",
    "refund",
    "return",
    "shipping",
    "tracking",
}


def load_dataset(path: Path) -> dict[str, Any]:
    """Load the routing dataset."""
    with path.open("r", encoding="utf-8") as handle:
        dataset = json.load(handle)

    if not isinstance(dataset, dict):
        raise TypeError("Routing dataset must contain a top-level JSON object.")

    return dataset


def tokenize(message: str) -> list[str]:
    """Normalize one message into lowercase lexical tokens."""
    return TOKEN_PATTERN.findall(message.casefold())


def token_set(message: str) -> set[str]:
    """Return non-stopword tokens for similarity analysis."""
    return {
        token
        for token in tokenize(message)
        if token not in STOPWORDS
    }


def jaccard_similarity(left: str, right: str) -> float:
    """Calculate token-set Jaccard similarity."""
    left_tokens = token_set(left)
    right_tokens = token_set(right)

    union = left_tokens | right_tokens
    if not union:
        return 1.0

    return len(left_tokens & right_tokens) / len(union)


def sequence_similarity(left: str, right: str) -> float:
    """Calculate normalized character-sequence similarity."""
    return SequenceMatcher(
        None,
        left.casefold().strip(),
        right.casefold().strip(),
    ).ratio()


def find_cross_split_near_duplicates(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Find suspiciously similar messages across different splits."""
    findings: list[dict[str, Any]] = []

    for left_index, left in enumerate(records):
        for right in records[left_index + 1 :]:
            if left["split"] == right["split"]:
                continue

            jaccard = jaccard_similarity(
                left["message"],
                right["message"],
            )
            sequence = sequence_similarity(
                left["message"],
                right["message"],
            )

            if (
                jaccard >= CROSS_SPLIT_JACCARD_THRESHOLD
                or sequence >= CROSS_SPLIT_SEQUENCE_THRESHOLD
            ):
                findings.append(
                    {
                        "left_case_id": left["case_id"],
                        "left_family_id": left["family_id"],
                        "left_split": left["split"],
                        "left_intent": left["expected_intent"],
                        "right_case_id": right["case_id"],
                        "right_family_id": right["family_id"],
                        "right_split": right["split"],
                        "right_intent": right["expected_intent"],
                        "jaccard_similarity": round(jaccard, 4),
                        "sequence_similarity": round(sequence, 4),
                    }
                )

    return sorted(
        findings,
        key=lambda finding: (
            max(
                finding["jaccard_similarity"],
                finding["sequence_similarity"],
            ),
            finding["left_case_id"],
            finding["right_case_id"],
        ),
        reverse=True,
    )


def find_class_associated_tokens(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Find vocabulary strongly associated with one intent label.

    The audit records both message-level frequency and semantic-family
    frequency so repeated variants from one family are not mistaken for
    broad class-level lexical shortcuts.
    """
    token_documents: dict[str, Counter[str]] = defaultdict(Counter)
    token_families: dict[str, dict[str, set[str]]] = {}

    for record in records:
        intent = record["expected_intent"]
        family_id = record["family_id"]

        document_tokens = {
            token
            for token in tokenize(record["message"])
            if token not in STOPWORDS
        }

        for token in document_tokens:
            token_documents[token][intent] += 1

            families_by_intent = token_families.setdefault(token, {})
            families_by_intent.setdefault(intent, set()).add(family_id)

    findings: list[dict[str, Any]] = []

    for token, intent_counts in token_documents.items():
        document_frequency = sum(intent_counts.values())

        if document_frequency < MIN_TOKEN_DOCUMENT_FREQUENCY:
            continue

        dominant_intent, dominant_count = intent_counts.most_common(1)[0]
        document_label_purity = dominant_count / document_frequency

        if document_label_purity < TOKEN_LABEL_PURITY_THRESHOLD:
            continue

        families_by_intent = token_families[token]

        family_intent_counts = {
            intent: len(family_ids)
            for intent, family_ids in families_by_intent.items()
        }

        distinct_family_count = sum(family_intent_counts.values())

        dominant_family_intent, dominant_family_count = max(
            family_intent_counts.items(),
            key=lambda item: item[1],
        )

        family_label_purity = (
            dominant_family_count / distinct_family_count
        )

        findings.append(
            {
                "token": token,
                "document_frequency": document_frequency,
                "dominant_intent": dominant_intent,
                "dominant_intent_count": dominant_count,
                "document_label_purity": round(
                    document_label_purity,
                    4,
                ),
                "document_intent_counts": dict(
                    sorted(intent_counts.items())
                ),
                "distinct_family_count": distinct_family_count,
                "dominant_family_intent": dominant_family_intent,
                "dominant_family_count": dominant_family_count,
                "family_label_purity": round(
                    family_label_purity,
                    4,
                ),
                "family_intent_counts": dict(
                    sorted(family_intent_counts.items())
                ),
                "families_by_intent": {
                    intent: sorted(family_ids)
                    for intent, family_ids
                    in sorted(families_by_intent.items())
                },
            }
        )

    return sorted(
        findings,
        key=lambda finding: (
            finding["distinct_family_count"],
            finding["family_label_purity"],
            finding["document_frequency"],
            finding["token"],
        ),
        reverse=True,
    )


def summarize_boundary_terms(
    records: list[dict[str, Any]],
) -> dict[str, dict[str, int]]:
    """Show whether important domain terms occur across intent classes."""
    summary: dict[str, dict[str, int]] = {}

    for boundary_term in sorted(BOUNDARY_TERMS):
        counts: Counter[str] = Counter()

        for record in records:
            if boundary_term in set(tokenize(record["message"])):
                counts[record["expected_intent"]] += 1

        summary[boundary_term] = {
            intent: counts.get(intent, 0)
            for intent in ("BUG", "PLATFORM", "OTHER")
        }

    return summary


def summarize_message_lengths(
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Summarize token counts overall and by intent."""
    overall_lengths = [
        len(tokenize(record["message"]))
        for record in records
    ]

    by_intent: dict[str, list[int]] = defaultdict(list)

    for record in records:
        by_intent[record["expected_intent"]].append(
            len(tokenize(record["message"]))
        )

    return {
        "overall": {
            "minimum": min(overall_lengths),
            "maximum": max(overall_lengths),
            "mean": round(
                sum(overall_lengths) / len(overall_lengths),
                2,
            ),
        },
        "by_intent": {
            intent: {
                "minimum": min(lengths),
                "maximum": max(lengths),
                "mean": round(sum(lengths) / len(lengths), 2),
            }
            for intent, lengths in sorted(by_intent.items())
        },
    }


def build_report(dataset: dict[str, Any]) -> dict[str, Any]:
    """Build the routing dataset QA report."""
    records = dataset.get("records")

    if not isinstance(records, list):
        raise TypeError("Dataset 'records' must be a JSON array.")

    cross_split_findings = find_cross_split_near_duplicates(records)
    class_tokens = find_class_associated_tokens(records)

    return {
        "report_id": "routing-intent-v1-audit",
        "dataset_id": dataset.get("dataset_id"),
        "dataset_version": dataset.get("version"),
        "input_provenance": dataset.get("provenance"),
        "evidence_class": "EXPERIMENTAL",
        "audit_scope": {
            "cross_split_near_duplicate_detection": {
                "jaccard_threshold": CROSS_SPLIT_JACCARD_THRESHOLD,
                "sequence_threshold": CROSS_SPLIT_SEQUENCE_THRESHOLD,
            },
            "class_associated_token_detection": {
                "minimum_document_frequency": (
                    MIN_TOKEN_DOCUMENT_FREQUENCY
                ),
                "document_label_purity_threshold": (
                    TOKEN_LABEL_PURITY_THRESHOLD
                ),
                "family_frequency_analysis": True,
                "interpretation": (
                    "Message-level frequency is reported together with "
                    "distinct semantic-family frequency so repeated variants "
                    "from one family can be distinguished from broader "
                    "class-level lexical associations."
                ),
            },
            "semantic_label_correctness": (
                "REQUIRES_HUMAN_REVIEW"
            ),
        },
        "summary": {
            "total_records": len(records),
            "cross_split_near_duplicate_findings": len(
                cross_split_findings
            ),
            "class_associated_token_findings": len(class_tokens),
            "cross_family_class_associated_token_findings": sum(
                finding["distinct_family_count"] > 1
                for finding in class_tokens
            ),
        },
        "message_length_summary": summarize_message_lengths(records),
        "boundary_term_distribution": summarize_boundary_terms(records),
        "cross_split_near_duplicates": cross_split_findings,
        "class_associated_tokens": class_tokens,
    }


def main() -> int:
    """Run the routing dataset quality audit."""
    try:
        dataset = load_dataset(DATASET_PATH)
        report = build_report(dataset)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print("Routing dataset audit FAILED")
        print(f"Reason: {exc}")
        return 1

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    summary = report["summary"]

    print("Routing dataset audit complete")
    print(f"Dataset: {DATASET_PATH.name}")
    print(f"Total records: {summary['total_records']}")
    print(
        "Cross-split near-duplicate findings: "
        f"{summary['cross_split_near_duplicate_findings']}"
    )
    print(
        "Strongly class-associated token findings: "
        f"{summary['class_associated_token_findings']}"
    )
    print(
        "Cross-family class-associated token findings: "
        f"{summary['cross_family_class_associated_token_findings']}"
    )
    print(f"Report: {RESULT_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())