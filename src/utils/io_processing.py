from __future__ import annotations

from src.configuration import logger, FIELD_ALIAS
from src.utils.data_classes import Address
from src.utils.str_utils import clean_string

alt_name_to_field = {
    value: key for key, values in FIELD_ALIAS.items() for value in values
}


def id_input_columns(headers: list[str]) -> str:
    """
    Attempts to match columns in the input data to expected address fields.
    Args:
        headers (str): column names from the input file
    Returns:
        col_map (dict):
            keys- address field names (or headers when no match is found)
            values- index of the column in the input data
    """

    clean_fields = [(idc, clean_string(raw_col)) for idc, raw_col in enumerate(headers)]
    col_map = {alt_name_to_field.get(col, col): idc for idc, col in clean_fields}
    return col_map


def validate_input_cols(col_map: dict) -> str:
    """Validates that the file received matches the expected
    format and can therefore be succeddfully processed.
    Args:
        col_map (dict): A dictionary with keys as the expected columns
            and values denoting the indices of the header in the input file.
    Returns:
        str: A message indicating the result of the validation."""
    warnings = []
    cols_found = set(col_map.keys())
    expected_columns = set(FIELD_ALIAS.keys())
    req_cols = [
        {"address_one", "locality", "state", "country"},
        {"latitude", "longitude"},
    ]

    unexpected_columns = cols_found - expected_columns
    missing_optional = expected_columns - cols_found
    missing_required = [col_set - cols_found for col_set in req_cols]
    if all(missing_required):
        msg = f"""Input invalid: please add either
                        {sorted(missing_required[1])} or {sorted(missing_required[0])}."""
        return False, msg

    if missing_optional:
        warnings.append(
            f"""Consider adding {sorted(missing_optional)}
                        to the input file for improved accuracy."""
        )
    if unexpected_columns:
        warnings.append(
            f"""Unexpected columns found: {sorted(unexpected_columns)}.
                        These columns might be misspelled or unneeded."""
        )
    if warnings:
        warning_message = "\n".join(warnings)
        logger.warning(warning_message)
        return True, warning_message
    return True, ""


def input_to_address(input_data: list, source: str = "file_input") -> list[Address]:
    headers = input_data[0]
    data = input_data[1:]
    if "source" not in headers:
        headers.append("source")
        for row in data:
            row.append(source)

    col_map = id_input_columns(headers)
    validated, msg = validate_input_cols(col_map)
    if not validated:
        logger.error(msg)
        return msg
    addresses = []
    for row in data:
        addr = Address()
        addr.from_data(row, col_map)
        addresses.append(addr)
    return addresses


def create_csv():
    """
    Creates a results file to be returned to
     the slack application/user
    """
    raise NotImplementedError


def stream_file():
    """
    Extracts file contents from IO stream
    """
    raise NotImplementedError
