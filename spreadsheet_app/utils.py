import os
import json
from spreadsheet_app.consts import VALID_TYPES, CONFIG_DIR, TypeTranslator


def check_schema_integrity(json_schema):
    error_message = None
    schema_is_valid = True

    if "columns" not in json_schema or not isinstance(json_schema["columns"], list):
        error_message = "Missing 'columns' field"
        schema_is_valid = False
    else:
        for col in json_schema["columns"]:
            if "name" not in col or "type" not in col:
                error_message = f"Column: {col}, is missing either 'name' or 'type' fields"
                schema_is_valid = False
                break

            if not isinstance(col["name"], str) or not col["name"]:
                error_message = f"Column: {col}, Can't have empty or none string name value"
                schema_is_valid = False
                break

            if col["type"] not in VALID_TYPES:
                error_message = f"Column: {col}, type is invalid. Type must be one of the following: " \
                    f"{', '.join(VALID_TYPES)}"
                schema_is_valid = False
                break

    return schema_is_valid, error_message


def validate_new_value_type(sheet_id, column_name, value):
    with open(f"{os.path.join(CONFIG_DIR, sheet_id)}.json", 'r') as f:
        config_schema = json.load(f)

        for col in config_schema['columns']:
            if col["name"] == column_name:
                if not isinstance(value, TypeTranslator[col["type"]].value):
                    return False

                return True
