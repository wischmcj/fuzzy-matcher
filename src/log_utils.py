import sys
import os
import logging

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
