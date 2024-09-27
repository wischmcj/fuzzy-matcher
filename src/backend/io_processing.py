from configuration import logger
from helper_classes import Address

FIELD_ALIAS = {
    "source_id": ["id", "record_id", "source_id"],
    "name": ["name", "full_name", "first_name", "last_name"],
    "address_one": [
        "address_one",
        "address",
        "street_address",
        "street",
        "address_line_1",
    ],
    "address_two": [
        "address_two",
        "additional_address",
        "address_cont",
        "address_line_2" "addl_address",
    ],
    "locality": ["locality", "city", "town"],
    "state": ["state", "province", "region"],
    "state_code": ["state_code", "state_abbr", "state_abbreviation"],
    "postal_code": ["zip", "zip_code", "postal_code", "postcode"],
    "country": ["country", "cntry", "nation"],
    "country_code": [
        "country_code",
        "short_country",
        "country_abbr",
        "country_abbreviation",
    ],
    "latitude": ["lat", "latitude"],
    "longitude": ["long", "longitude"],
}

values_to_field = {
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
    stdize = lambda x: x.lower().strip().replace(" ", "_")
    clean_fields = [(idc, stdize(raw_col)) for idc, raw_col in enumerate(headers)]
    col_map = {values_to_field.get(col, col): idc for idc, col in clean_fields}
    return col_map


def validate_input_cols(col_map: dict) -> str:
    """Validates that the file recieved matches the expected
    format and can therefore be succeddfully processed.
    Args:
        col_map (dict): A dictionary with keys as the expected columns
            and values denoting the indicies of the header in the input file.
    Returns:
        str: A message indicating the result of the validation."""
    warnings = []
    cols_found = set(col_map.keys())
    expected_columns = set(FIELD_ALIAS.keys())
    req_cols = [
        ["address_one", "locality", "state", "country"],
        ["latitude", "longitude"],
    ]

    unexpected_columns = cols_found - expected_columns
    missing_optional = expected_columns - cols_found
    missing_required = [col_set.intersection(cols_found) for col_set in req_cols]

    if all(missing_required):
        msg = f"""Input invalid: please add either 
                        {missing_required[1]} or {missing_required[0]}."""
        return msg

    if missing_optional:
        warnings.append(f"""Consider adding {missing_optional}
                        to the input file for improved accuracy.""")
    if unexpected_columns:
        warnings.append(f"""Unexpected columns found: {unexpected_columns}.
                        These columns might be misspelled or unneeded.""")
    if warnings:
        warning_message = "\n".join(warnings)
        logger.warning(warning_message)
        return warning_message
    return "Validated"


def input_to_address(input_data: list) -> list[Address]:
    headers = input_data[0]
    data = input_data[1:]
    col_map = id_input_columns(headers)
    validation_status = validate_input_cols(col_map)

    if validation_status != "Validated":
        logger.error(validation_status)
        return validation_status

    addresses = [Address(row, col_map) for row in data]
    return addresses
