from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

from toml import load

sys.path.insert(0, str(Path(__file__).parent.parent))

# configuration variables

root_dir = "src/" if os.environ["FULL_PATH"] == "True" else ""
os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
os.environ.get("INPUT_DIR", ".")
os.environ.get("OUTPUT_DIR", ".")

# Configurable settings
with open(f"{root_dir}config.toml") as f:
    CONFIG = load(f)

LOCAL_FILENAME = CONFIG["local_filename"]


logger = logging.getLogger("pmt_fuzzy")

if os.environ["FULL_PATH"] == "True":
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
