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


def validate_lookup_loop(sheet_id, spreadsheet, column_name, cell_index, lookup_expression):
    def fix_type(col_name, final_expression):
        with open(f"{os.path.join(CONFIG_DIR, sheet_id)}.json", 'r') as f:
            config_schema = json.load(f)

            for col in config_schema["columns"]:
                if col["name"] == col_name:
                    try:
                        return_value = TypeTranslator[col["type"]].value(final_expression)
                    except ValueError:
                        try:
                            return_value = TypeTranslator[col["type"]].value(float(final_expression))
                        except ValueError:
                            return_value = final_expression

                    return return_value

    visited_nodes = {(column_name, cell_index): None}

    while isinstance(lookup_expression, str) and "lookup" in lookup_expression:
        extracted_parts = lookup_expression.replace("lookup(", "").rstrip(")").split(",")
        extracted_col, extracted_index = extracted_parts[0], int(extracted_parts[1])

        if (extracted_col, extracted_index) in visited_nodes:
            return False

        lookup_expression = spreadsheet.at[extracted_index, extracted_col]
        visited_nodes[extracted_col, extracted_index] = None

    lookup_expression = fix_type(extracted_col, lookup_expression)

    return validate_new_value_type(sheet_id, column_name, lookup_expression)


def evaluate_lookup(spreadsheet, lookup_expression):
    while isinstance(lookup_expression, str) and "lookup" in lookup_expression:
        extracted_parts = lookup_expression.replace("lookup(", "").rstrip(")").split(",")
        extracted_col, extracted_index = extracted_parts[0], int(extracted_parts[1])

        lookup_expression = spreadsheet.at[extracted_index, extracted_col]

    return lookup_expression


def get_type_dictionary(sheet_id):
    """This function is mainly used in order to allow multiple data types in a single column when using pandas.
    It is necessary in order to not change the int values being inserted into float64 (because this is the default
    behaviour of a pandas dataframe).
    """

    dtype_dict = {}

    with open(f"{os.path.join(CONFIG_DIR, sheet_id)}.json", 'r') as f:
        config_schema = json.load(f)
        for col in config_schema['columns']:
            dtype_dict[col["name"]] = object

    return dtype_dict
