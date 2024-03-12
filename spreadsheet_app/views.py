from spreadsheet_app.spreadsheet import create_new_sheet, set_cell_value, get_spreadsheet_values
from spreadsheet_app import app
from flask import request, jsonify


@app.route('/sheet', methods=["POST"])
def create_sheet():
    new_sheet_json = request.get_json()

    try:
        sheet_id = create_new_sheet(new_sheet_json)
    except ValueError as e:
        response = (f"Invalid json schema: {e}", 400)
    else:
        response = (sheet_id, 201)

    return response


@app.route("/sheet", methods=["PUT"])
def set_cell():
    request_data = request.get_json()

    try:
        sheet_id = request_data["sheet_id"]
        column_name = request_data["column_name"]
        cell_index = request_data["cell_index"]
        value = request_data["value"]

        set_cell_value(sheet_id, column_name, cell_index, value)
    except TypeError as e:
        response = (f"Invalid value for specified cell: {e}", 400)
    except LookupError as e:
        response = (f"Invalid lookup expression: {e}", 400)
    else:
        response = (f"Cell value set successfully", 200)

    return response


@app.route("/sheet/<sheet_id>", methods=["GET"])
def get_spreadsheet(sheet_id):
    try:
        response = (get_spreadsheet_values(sheet_id), 200)
    except ValueError as e:
        response = (f"Invalid sheet ID: {e}", 400)

    return response
