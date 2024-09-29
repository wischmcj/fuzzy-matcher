from __future__ import annotations

import string
import sys
from pathlib import Path

from pytest import mark

sys.path.insert(0, str(Path(__file__).parent.parent))

import src.utils.io_processing as io_module  # noqa: E402


def string_compare(s1, s2) -> bool:
    remove = string.punctuation + string.whitespace
    return s1.translate(remove) == s2.translate(remove)


@mark.parametrize(
    "headers, expected",
    [
        (
            [
                "record_id",
                "full_name",
                "street_address",
                "town",
                "province",
                "nation",
            ],
            {
                "source_id": 0,
                "name": 1,
                "address_one": 2,
                "locality": 3,
                "state": 4,
                "country": 5,
            },
        ),
        (
            ["id", "name", "address", "city", "state", "country"],
            {
                "source_id": 0,
                "name": 1,
                "address_one": 2,
                "locality": 3,
                "state": 4,
                "country": 5,
            },
        ),
        (
            ["record_id", "full_name", "street_address", "town", "province", "nation"],
            {
                "source_id": 0,
                "name": 1,
                "address_one": 2,
                "locality": 3,
                "state": 4,
                "country": 5,
            },
        ),
        (
            ["id", "name", "address", "city", "state", "country", "extra"],
            {
                "source_id": 0,
                "name": 1,
                "address_one": 2,
                "locality": 3,
                "state": 4,
                "country": 5,
                "extra": 6,
            },
        ),
        (
            ["id", "name", "address", "city", "state"],
            {"source_id": 0, "name": 1, "address_one": 2, "locality": 3, "state": 4},
        ),
    ],
)
def test_id_input_columns(headers, expected):
    actual = io_module.id_input_columns(headers)
    assert actual == expected


@mark.parametrize(
    "col_map, expected",
    [
        (
            {
                "source_id": 0,
                "name": 1,
                "address_one": 2,
                "locality": 3,
                "state": 4,
            },
            (
                False,
                "Input invalid: please add either\n                        ['latitude', 'longitude'] or ['country'].",
            ),
        ),
        (
            {
                "source_id": 0,
                "name": 1,
                "address_one": 2,
                "locality": 3,
                "state": 4,
                "country": 5,
            },
            (
                True,
                "Consider adding ['address_two', 'country_code', 'latitude', 'longitude', 'postal_code', 'source', 'state_code']\n                        to the input file for improved accuracy.",
            ),
        ),
        (
            {
                "source_id": 0,
                "name": 1,
                "address_one": 2,
                "locality": 3,
                "state": 4,
                "country": 5,
                "extra": 6,
            },
            (
                True,
                "Consider adding ['address_two', 'country_code', 'latitude', 'longitude', 'postal_code', 'source', 'state_code']\n                        to the input file for improved accuracy.\nUnexpected columns found: ['extra'].\n                        These columns might be misspelled or unneeded.",
            ),
        ),
    ],
)
def test_validate_input_cols(col_map, expected):
    actual = io_module.validate_input_cols(col_map)
    assert string_compare(actual[1], expected[1])


@mark.parametrize(
    "input_data, expected",
    [
        (
            [
                ["id", "name", "address", "city", "state"],
                ["1", "John Doe", "123 Main St", "Anytown", "Anystate"],
            ],
            "Input invalid: please add either\n                        ['latitude', 'longitude'] or ['country'].",
        ),
        (
            [
                ["id", "name", "address", "city", "state", "country"],
                ["1", "John Doe", "123 Main St", "Anytown", "Anystate", "USA"],
            ],
            [
                io_module.Address(
                    source="file_input",
                    source_id="1",
                    name="John Doe",
                    address_one="123 Main St",
                    address_two=None,
                    locality="Anytown",
                    state="Anystate",
                    state_code=None,
                    postal_code=None,
                    country="USA",
                    country_code=None,
                    latitude=None,
                    longitude=None,
                    lat_long=(None, None),
                    full_address="123 Main St",
                )
            ],
        ),
        (
            [
                [
                    "record_id",
                    "full_name",
                    "street_address",
                    "town",
                    "province",
                    "nation",
                ],
                ["1", "John Doe", "123 Main St", "Anytown", "Anystate", "USA"],
            ],
            [
                io_module.Address(
                    source="file_input",
                    source_id="1",
                    name="John Doe",
                    address_one="123 Main St",
                    address_two=None,
                    locality="Anytown",
                    state="Anystate",
                    state_code=None,
                    postal_code=None,
                    country="USA",
                    country_code=None,
                    latitude=None,
                    longitude=None,
                    lat_long=(None, None),
                    full_address="123 Main St",
                )
            ],
        ),
    ],
)
def test_input_to_address(input_data, expected):
    actual = io_module.input_to_address(input_data)
    assert actual == expected
