import os
import uuid
import json
import pandas as pd
from spreadsheet_app.consts import BASE_DATA_PATH
from spreadsheet_app.utils import check_schema_integrity


def create_new_sheet(json_schema):
    schema_is_valid, error_message = check_schema_integrity(json_schema)

    if not schema_is_valid:
        raise ValueError(error_message)

    new_sheet_id = str(uuid.uuid4())

    config_dir = os.path.join(BASE_DATA_PATH, "configs")
    sheets_dir = os.path.join(BASE_DATA_PATH, "sheets")
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(sheets_dir, exist_ok=True)

    with open(f"{os.path.join(config_dir, new_sheet_id)}.json", "w") as f:
        json.dump(json_schema, f)

    columns = json_schema["columns"]
    empty_df = pd.DataFrame(columns=[col["name"] for col in columns])

    empty_df.to_csv(f"{os.path.join(sheets_dir, new_sheet_id)}.csv")

    return new_sheet_id
