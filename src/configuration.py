from toml import load
import os

root_dir = "src/" if os.environ["FULL_PATH"] == "True" else ""
os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
os.environ.get("INPUT_DIR", ".")
os.environ.get("OUTPUT_DIR", ".")

# Configurable settings
with open(f"{root_dir}config.toml", "r") as f:
    CONFIG = load(f)

LOCAL_FILENAME = CONFIG["local_filename"]
