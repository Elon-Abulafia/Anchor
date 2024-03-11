from app import app, request, jsonify


@app.route('/')
def hello_world():
    return 'Hello World!'

#
# @app.route('/sheet', methods=['POST'])
# def create_sheet():
#     new_sheet_json = request.json()
