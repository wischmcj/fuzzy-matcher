from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from toml import load

sys.path.insert(0, str(Path(__file__).parent.parent))

# environment variables
ROOT_DIR = "src/" if os.environ.get("FULL_PATH", "False") == "True" else ""
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
INPUT_DIR = "".join([ROOT_DIR, os.environ.get("INPUT_DIR", ".")])
OUTPUT_DIR = "".join([ROOT_DIR, os.environ.get("OUTPUT_DIR", ".")])

# Configurable settings
with open(f"{ROOT_DIR}config.toml") as f:
    CONFIG = load(f)

LOCAL_FILENAME = CONFIG["local_filename"]
FIELD_ALIAS = CONFIG["field_aliases"]

# Logging configuration
logger = logging.getLogger("pmt_fuzzy")

if os.environ.get("FULL_PATH", "False") == "True":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# in the case of a local run level =logging.DEBUG
else:
    level = logging.DEBUG
    logger.info("logger set to DEBUG..")
for handler in logger.handlers:
    handler.setLevel(level)
    logger.info("logger set to INFO..")
for handler in logger.handlers:
    handler.setLevel(level)
