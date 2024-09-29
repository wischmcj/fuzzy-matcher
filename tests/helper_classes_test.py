from __future__ import annotations

import logging
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.backend.helper_classes import Address, MatchTuple  # noqa: E402

logger = logging.getLogger(__name__)


# Define the fixtures
# These fixtures represent multiple different test cases.
# Tests using these fixtures will loop over each
#  possible value (params) for each fixture and will
#  run the test once for each of these values.
@pytest.fixture(
    params=[
        ["1", "John Doe", "123 Main St", "Anytown", "Anystate", "USA"],
        ["2", "Jane Smith", "456 Oak St", "Sometown", "Somestate", "USA"],
        ["3", "Bob Johnson", "789 Pine St", "Othertown", "Otherstate", "USA"],
    ]
)
def search_address(request):
    addr = Address()
    addr.from_data(
        request.param,
        {
            "source_id": 0,
            "name": 1,
            "address_one": 2,
            "locality": 3,
            "state": 4,
            "country": 5,
        },
    )
    return addr


@pytest.fixture(
    params=[
        ["4", "Jane Doe", "123 Main St", "Anytown", "Anystate", "USA"],
        ["5", "John Smith", "456 Oak St", "Sometown", "Somestate", "USA"],
        ["6", "Alice Johnson", "789 Pine St", "Othertown", "Otherstate", "USA"],
    ]
)
def matched_address(request):
    addr = Address()
    addr.from_data(
        request.param,
        {
            "source_id": 0,
            "name": 1,
            "address_one": 2,
            "locality": 3,
            "state": 4,
            "country": 5,
        },
    )
    return addr


expected_outputs_init = {
    "123 Main St": {
        "123 Main St": {
            "ratio": 100,
            "partial_ratio": 100,
            "token_sort_ratio": 100,
            "token_set_ratio": 100,
            "partial_token_sort_ratio": 100,
            "partial_token_set_ratio": 100,
        },
        "456 Oak St": {
            "ratio": 48,
            "partial_ratio": 56,
            "token_sort_ratio": 48,
            "token_set_ratio": 48,
            "partial_token_sort_ratio": 56,
            "partial_token_set_ratio": 100,
        },
        "789 Pine St": {
            "ratio": 55,
            "partial_ratio": 63,
            "token_sort_ratio": 55,
            "token_set_ratio": 55,
            "partial_token_sort_ratio": 63,
            "partial_token_set_ratio": 100,
        },
    },
    "456 Oak St": {
        "123 Main St": {
            "ratio": 48,
            "partial_ratio": 56,
            "token_sort_ratio": 48,
            "token_set_ratio": 48,
            "partial_token_sort_ratio": 56,
            "partial_token_set_ratio": 100,
        },
        "456 Oak St": {
            "ratio": 100,
            "partial_ratio": 100,
            "token_sort_ratio": 100,
            "token_set_ratio": 100,
            "partial_token_sort_ratio": 100,
            "partial_token_set_ratio": 100,
        },
        "789 Pine St": {
            "ratio": 38,
            "partial_ratio": 46,
            "token_sort_ratio": 38,
            "token_set_ratio": 38,
            "partial_token_sort_ratio": 46,
            "partial_token_set_ratio": 100,
        },
    },
    "789 Pine St": {
        "123 Main St": {
            "ratio": 55,
            "partial_ratio": 63,
            "token_sort_ratio": 55,
            "token_set_ratio": 55,
            "partial_token_sort_ratio": 63,
            "partial_token_set_ratio": 100,
        },
        "456 Oak St": {
            "ratio": 38,
            "partial_ratio": 46,
            "token_sort_ratio": 38,
            "token_set_ratio": 38,
            "partial_token_sort_ratio": 46,
            "partial_token_set_ratio": 100,
        },
        "789 Pine St": {
            "ratio": 100,
            "partial_ratio": 100,
            "token_sort_ratio": 100,
            "token_set_ratio": 100,
            "partial_token_sort_ratio": 100,
            "partial_token_set_ratio": 100,
        },
    },
}


# Use the fixtures in the tests
def test_match_tuple_init(search_address, matched_address):
    match_tuple = MatchTuple(search_address, matched_address)
    expected = expected_outputs_init[match_tuple.search_address.full_address][
        match_tuple.matched_address.full_address
    ]
    assert expected == match_tuple.fuzz_stats


def test_match_tuple_getitem(search_address, matched_address):
    match_tuple = MatchTuple(search_address, matched_address)
    assert match_tuple["search_address"] == search_address


def test_match_tuple_eq(search_address, matched_address):
    match_tuple1 = MatchTuple(search_address, matched_address)
    match_tuple2 = MatchTuple(search_address, matched_address)
    assert match_tuple1 == match_tuple2


def test_match_tuple_differs(search_address, matched_address):
    match_tuple1 = MatchTuple(search_address, search_address)
    match_tuple2 = MatchTuple(search_address, matched_address)
    if search_address.full_address != matched_address.full_address:
        # If the full addresses are different, the match should differ
        assert match_tuple1.differs(match_tuple2, "avg_fuzz_score") == "gt"
        assert match_tuple2.differs(match_tuple1, "avg_fuzz_score") == "lt"
    else:
        # If the full addresses are the same, the match should not differ
        assert match_tuple1.differs(match_tuple2, "avg_fuzz_score") == "eq"


def test_match_tuple_compare(search_address, matched_address):
    match_tuple1 = MatchTuple(search_address, matched_address)
    match_tuple2 = MatchTuple(search_address, matched_address)
    assert match_tuple1.compare(match_tuple2) == "same"
