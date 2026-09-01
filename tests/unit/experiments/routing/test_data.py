"""Unit tests for the routing benchmark data boundary."""

from dataclasses import fields

from experiments.routing.benchmark.data import (
    ModelExample,
    load_routing_records,
    model_examples_for_split,
    records_for_split,
)


def test_frozen_dataset_loads_expected_record_count() -> None:
    records = load_routing_records()

    assert len(records) == 180


def test_frozen_dataset_preserves_expected_split_counts() -> None:
    records = load_routing_records()

    assert len(records_for_split(records, "train")) == 108
    assert len(records_for_split(records, "validation")) == 36
    assert len(records_for_split(records, "test")) == 36


def test_model_examples_expose_only_message_and_target() -> None:
    exposed_fields = {
        field.name
        for field in fields(ModelExample)
    }

    assert exposed_fields == {
        "message",
        "expected_intent",
    }


def test_training_examples_preserve_training_labels() -> None:
    records = load_routing_records()
    training_records = records_for_split(records, "train")
    training_examples = model_examples_for_split(records, "train")

    assert len(training_examples) == len(training_records)

    assert [
        example.expected_intent
        for example in training_examples
    ] == [
        record.expected_intent
        for record in training_records
    ]


def test_training_examples_preserve_customer_messages() -> None:
    records = load_routing_records()
    training_records = records_for_split(records, "train")
    training_examples = model_examples_for_split(records, "train")

    assert [
        example.message
        for example in training_examples
    ] == [
        record.message
        for record in training_records
    ]
