from spreadsheet_app.spreadsheet import create_new_sheet
from spreadsheet_app import app
from flask import request, jsonify


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/sheet', methods=['POST'])
def create_sheet():
    new_sheet_json = request.get_json()

    try:
        sheet_id = create_new_sheet(new_sheet_json)
    except ValueError as e:
        response = (f"Invalid json schema: {e}", 400)
    else:
        response = (sheet_id, 200)

    return response
