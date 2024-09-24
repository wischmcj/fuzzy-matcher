import csv
import os
from file_tasks import process_records

from configuration import LOCAL_FILENAME


def read_from_csv():
    """Reads data from local input file"""
    # LOCAL ENTRYPOINT
    with open(f"data/in/{LOCAL_FILENAME}.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        data = [row for row in reader]
        name = os.path.basename(f.name)
        process_records(data, local=True, executor=None, name=name)


if __name__ == "__main__":
    os.environ["FULL_PATH"] = "True"
    read_from_csv()
