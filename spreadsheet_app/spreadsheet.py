import os
import uuid
import json
import pandas as pd
from spreadsheet_app.utils import check_schema_integrity, validate_new_value_type, validate_lookup_loop, \
    evaluate_lookup, get_type_dictionary
from spreadsheet_app.consts import CONFIG_DIR, SHEETS_DIR, TypeTranslator


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
    sheet_path = f"{os.path.join(SHEETS_DIR, sheet_id)}.csv"
    spreadsheet = pd.read_csv(sheet_path, index_col=0)

    if isinstance(value, str) and "lookup" in value:
        if not validate_lookup_loop(sheet_id, spreadsheet, column_name, cell_index, value):
            raise LookupError("Encountered infinite loop or invalid type while trying to insert new lookup expression")
    elif not validate_new_value_type(sheet_id, column_name, value):
        raise TypeError("Cell value type must match column type")

    spreadsheet.at[cell_index, column_name] = value
    spreadsheet.to_csv(sheet_path)


def get_spreadsheet_values(sheet_id):
    resulting_dict = {}
    sheet_path = f"{os.path.join(SHEETS_DIR, sheet_id)}.csv"

    with open(f"{os.path.join(CONFIG_DIR, sheet_id)}.json", 'r') as f:
        config_schema = json.load(f)
        type_schema = {col["name"]: TypeTranslator[col["type"]].value for col in config_schema["columns"]}

    try:
        spreadsheet = pd.read_csv(sheet_path, index_col=0)
    except FileNotFoundError as e:
        raise e

    for (index, col), value in spreadsheet.stack().items():
        if isinstance(value, str) and "lookup" in value:
            value = evaluate_lookup(spreadsheet, value)

        try:
            resulting_dict[str((col, index))] = type_schema[col](value)
        except ValueError:
            resulting_dict[str((col, index))] = type_schema[col](float(value))

    return resulting_dict
