from configuration import logger
from src.backend.io_processing import input_to_address
from matching.main import match_address


def create_csv():
    raise NotImplementedError


def stream_file():
    raise NotImplementedError


def process_file_urls(urls: list):
    match_files = []
    for url in urls:
        data = stream_file(url)
        match_file = process_records(data)
        match_files.append(match_file)
    return match_files


def process_records(data: list) -> list[dict]:
    input_addresses = input_to_address(data)
    match_list = []
    for address in input_addresses:
        match = match_address(address)
        match_list.append(match)

    match_file = create_csv(match_list)

    return match_file
