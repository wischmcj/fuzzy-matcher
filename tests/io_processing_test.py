from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from pytest import mark
import src.backend.io_processing as io_module

import string

def string_compare(s1, s2)-> bool:
    remove = string.punctuation + string.whitespace
    return s1.translate(None, remove) == s2.translate(None, remove)

@mark.parametrize(
    "headers, expected",
    [
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
                "country": 5,
            },
            "Validated",
        ),
        (
            {"source_id": 0, "name": 1, "address_one": 2, "locality": 3, "state": 4},
            "Input invalid: please add either \n                        ['country'] or ['latitude', 'longitude'].",
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
            "Unexpected columns found: {'extra'}.\n                        These columns might be misspelled or unneeded.",
        ),
    ],
)
def test_validate_input_cols(col_map, expected):
    actual = io_module.validate_input_cols(col_map)
    assert actual == expected


@mark.parametrize(
    "input_data, expected",
    [
        (
            [
                ["id", "name", "address", "city", "state", "country"],
                ["1", "John Doe", "123 Main St", "Anytown", "Anystate", "USA"],
            ],
            [
                io_module.Address(
                    ["1", "John Doe", "123 Main St", "Anytown", "Anystate", "USA"],
                    {
                        "source_id": 0,
                        "name": 1,
                        "address_one": 2,
                        "locality": 3,
                        "state": 4,
                        "country": 5,
                    },
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
                    ["1", "John Doe", "123 Main St", "Anytown", "Anystate", "USA"],
                    {
                        "source_id": 0,
                        "name": 1,
                        "address_one": 2,
                        "locality": 3,
                        "state": 4,
                        "country": 5,
                    },
                )
            ],
        ),
        (
            [
                ["id", "name", "address", "city", "state"],
                ["1", "John Doe", "123 Main St", "Anytown", "Anystate"],
            ],
            "Input invalid: please add either \n                        ['country'] or ['latitude', 'longitude'].",
        ),
    ],
)
def test_input_to_address(input_data, expected):
    actual = io_module.input_to_address(input_data)
    assert actual == expected
