import os
import uuid
import json
import pandas as pd
from spreadsheet_app.utils import check_schema_integrity, validate_new_value_type
from spreadsheet_app.consts import CONFIG_DIR, SHEETS_DIR


def create_new_sheet(json_schema):
    schema_is_valid, error_message = check_schema_integrity(json_schema)

    if not schema_is_valid:
        raise ValueError(error_message)

    new_sheet_id = str(uuid.uuid4())

    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(SHEETS_DIR, exist_ok=True)

    with open(f"{os.path.join(CONFIG_DIR, new_sheet_id)}.json", "w") as f:
        json.dump(json_schema, f)

    columns = json_schema["columns"]
    empty_df = pd.DataFrame(columns=[col["name"] for col in columns])

    empty_df.to_csv(f"{os.path.join(SHEETS_DIR, new_sheet_id)}.csv")

    return new_sheet_id


def set_cell_value(sheet_id, column_name, cell_index, value):
    if validate_new_value_type(sheet_id, column_name, value):
        sheet_path = f"{os.path.join(SHEETS_DIR, sheet_id)}.csv"

        spreadsheet = pd.read_csv(sheet_path, index_col=0)
        spreadsheet.at[cell_index, column_name] = value

        print(spreadsheet)
        spreadsheet.to_csv(sheet_path)
    else:
        raise TypeError("Cell value type must match column type")
