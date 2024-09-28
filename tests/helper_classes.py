import pytest
from src.backend.helper_classes import MatchTuple, Address
from fuzzywuzzy.fuzz import ratio, partial_ratio, token_sort_ratio, token_set_ratio, partial_token_sort_ratio, partial_token_set_ratio




def test_match_tuple_init():
    search_address = Address(["1", "John Doe", "123 Main St", "Anytown", "Anystate", "USA"],
                                {"source_id": 0, "name": 1, "address_one": 2, "locality": 3, "state": 4, "country": 5})
    matched_address = Address(["2", "Jane Doe", "123 Main St", "Anytown", "Anystate", "USA"],
                                {"source_id": 0, "name": 1, "address_one": 2, "locality": 3, "state": 4, "country": 5})
    match_tuple = MatchTuple(search_address, matched_address, [("name", "John Doe")])
    assert match_tuple.search_address == search_address
    assert match_tuple.matched_address == matched_address
    assert match_tuple.cols_matched == [("name", "John Doe")]
    assert match_tuple.fuzz_stats is not None

def test_match_tuple_getitem():
    search_address = Address(["1", "John Doe", "123 Main St", "Anytown", "Anystate", "USA"],
                                {"source_id": 0, "name": 1, "address_one": 2, "locality": 3, "state": 4, "country": 5})
    matched_address = Address(["2", "Jane Doe", "123 Main St", "Anytown", "Anystate", "USA"],
                                {"source_id": 0, "name": 1, "address_one": 2, "locality": 3, "state": 4, "country": 5})
    match_tuple = MatchTuple(search_address, matched_address, [("name", "John Doe")])
    assert match_tuple["search_address"] == search_address

def test_match_tuple_eq():
    search_address = Address(["1", "John Doe", "123 Main St", "Anytown", "Anystate", "USA"],
                                {"source_id": 0, "name": 1, "address_one": 2, "locality": 3, "state": 4, "country": 5})
    matched_address = Address(["2", "Jane Doe", "123 Main St", "Anytown", "Anystate", "USA"],
                                {"source_id": 0, "name": 1, "address_one": 2, "locality": 3, "state": 4, "country": 5})
    match_tuple1 = MatchTuple(search_address, matched_address, [("name", "John Doe")])
    match_tuple2 = MatchTuple(search_address, matched_address, [("name", "John Doe")])
    assert match_tuple1 == match_tuple2

def test_match_tuple_differs():
    search_address = Address(["1", "John Doe", "123 Main St", "Anytown", "Anystate", "USA"],
                                {"source_id": 0, "name": 1, "address_one": 2, "locality": 3, "state": 4, "country": 5})
    matched_address = Address(["2", "Jane Doe", "123 Main St", "Anytown", "Anystate", "USA"],
                                {"source_id": 0, "name": 1, "address_one": 2, "locality": 3, "state": 4, "country": 5})
    match_tuple1 = MatchTuple(search_address, matched_address, [("name", "John Doe")])
    match_tuple2 = MatchTuple(search_address, matched_address, [("name", "John Doe")])
    assert match_tuple1.differs(match_tuple2, "search_address") is None

def test_match_tuple_compare():
    search_address = Address(["1", "John Doe", "123 Main St", "Anytown", "Anystate", "USA"],
                                {"source_id": 0, "name": 1, "address_one": 2, "locality": 3, "state": 4, "country": 5})
    matched_address = Address(["2", "Jane Doe", "123 Main St", "Anytown", "Anystate", "USA"],
                                {"source_id": 0, "name": 1, "address_one": 2, "locality": 3, "state": 4, "country": 5})
    match_tuple1 = MatchTuple(search_address, matched_address, [("name", "John Doe")])
    match_tuple2 = MatchTuple(search_address, matched_address, [("name", "John Doe")])
    assert match_tuple1.compare(match_tuple2) == 'same'