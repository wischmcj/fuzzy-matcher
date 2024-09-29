from __future__ import annotations

import csv
import os
from concurrent.futures import Executor

from configuration import LOCAL_FILENAME, INPUT_DIR
from matching import match_address
from utils.io_processing import input_to_address, create_csv, stream_file


def read_local_file():
    """Reads data from local input file
    Used to pilot functionality locally"""
    with open(f"{INPUT_DIR}/{LOCAL_FILENAME}.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        data = [row for row in reader]
        name = os.path.basename(f.name)
        process_records(data, local=True, executor=None, name=name)


def process_file_urls(urls: list, executor: Executor | None = None):
    match_files = []
    for url in urls:
        data = stream_file(url)
        match_file = process_records(data, executor)
        match_files.append(match_file)
    return match_files


def process_records(data: list, executor: Executor | None = None) -> list[dict]:
    input_addresses = input_to_address(data)
    if executor:
        match_list = list(executor.map(match_address, input_addresses))
    else:
        match_list = []
        for address in input_addresses:
            match = match_address(address)
            match_list.append(match)

        match_file = create_csv(match_list)

    return match_file


if __name__ == "__main__":
    read_local_file()
