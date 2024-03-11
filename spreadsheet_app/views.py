from spreadsheet_app.spreadsheet import create_new_sheet, set_cell_value
from spreadsheet_app import app
from flask import request, jsonify


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/sheet', methods=["POST"])
def create_sheet():
    new_sheet_json = request.get_json()

    try:
        sheet_id = create_new_sheet(new_sheet_json)
    except ValueError as e:
        response = (f"Invalid json schema: {e}", 400)
    else:
        response = (sheet_id, 200)

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
    else:
        response = (f"Cell value set successfully", 200)

    return response
