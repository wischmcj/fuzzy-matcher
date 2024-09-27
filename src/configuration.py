from toml import load
import os
import sys
import os
import logging

# configuration variables 

root_dir = "src/" if os.environ["FULL_PATH"] == "True" else ""
os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
os.environ.get("INPUT_DIR", ".")
os.environ.get("OUTPUT_DIR", ".")

# Configurable settings
with open(f"{root_dir}config.toml", "r") as f:
    CONFIG = load(f)

LOCAL_FILENAME = CONFIG["local_filename"]



logger = logging.getlogger("pmt_fuzzy")

if os.environ("FULL_PATH") == "True":
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
