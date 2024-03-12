import os

VALID_TYPES = ["boolean", "int", "double", "string"]
BASE_DATA_PATH = os.environ.get("BASE_DATA_PATH", "Example/Path")
CONFIG_DIR = os.path.join(BASE_DATA_PATH, "configs")
SHEETS_DIR = os.path.join(BASE_DATA_PATH, "sheets")
