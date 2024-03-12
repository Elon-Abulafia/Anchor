# Anchor Home Assignment
###Base Assumptions
- Support only 4 basic types for the intial state of the application (boolean, int, double, string)
- GetSheet returns the requested sheet without modifying the output (Meaning it will return a normal dictionary)
- When setting a new cell except for the `value` field, everything else is valid 

###Running Tests
In order to run the tests of the application, make sure you are in the correct location at the head of the directory (Anchor) and run the following command:
```
python run_tests.py
```

###Running The Application
In order to run the application, clone the repository and run the following commands from within the directory:
```bash
pip install -r requirements.txt
python run.py
```
If you want the newly created spreadsheet files to be saved in a location other than the default one (Example/Path/sheets...), you can change the environment variable `BASE_DATA_PATH` as you see fit.

####Application Endpoints
- `/sheet` is the base path for the application and will do different things depending on the type of the request.
    - A `POST` request will create a new spreadsheet according to a given config schema
    - A `PUT` request will set a cell in an existing spreadsheet
    - A `GET` request will return the values of an existing spreadsheet
    
###How To Use Each Endpoint
#####`POST`
In order to create a new spreadsheet, you need the send a `POST` request with a `json` body, representing the config schema, of the following structure:
```json
{
  "columns": [
    {
      "name": "A",
      "type": "boolean"
    },
    {
      "name": "B",
      "type": "int"
    },
    {
      "name": "C",
      "type": "double"
    },
    {
      "name": "D",
      "type": "string"
    }
  ]
}
```
#####`PUT`
In order to insert a new cell, you will need to send a `PUT` request with a `json` body of the following structure:
```
{
    "sheet_id": "example-sheet-id",
    "column_name": "example-column",
    "cell_index": <example_index>,
    "value": "example value"
}
```

#####`GET`
In order to get an existing spreadsheet, you will need to send a `GET` request with the sheet id in the url params, e.g:
```
http://localhost:5000/sheet/<sheet_id>
```