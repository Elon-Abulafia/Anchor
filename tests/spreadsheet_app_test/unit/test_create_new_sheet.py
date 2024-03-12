import unittest
from unittest.mock import patch
from tests.consts import COLUMN_NAMES
from spreadsheet_app.spreadsheet import create_new_sheet


def fixed_uuid():
    return "fixed-uuid"


class CreateNewSheetTest(unittest.TestCase):
    def setUp(self) -> None:
        valid_types = ["boolean", "int", "double", "string"]

        self.test_data = {
            "valid": [{
                "data": {"columns": [
                    {"name": col_name, "type": t} for col_name, t in zip(COLUMN_NAMES, valid_types)
                ]},
                "expected_result": fixed_uuid()
            }],
            "invalid": [
                {"data": {"c": "Missing columns key"},
                 "expected_result": {"type": ValueError,
                                     "message": "Missing 'columns' field or it is empty"}},
                {"data": {"columns": []},
                 "expected_result": {"type": ValueError,
                                     "message": "Missing 'columns' field or it is empty"}},
                {"data":
                     {"columns": [{"name": "X", "type": "invalid_type"}]},
                 "expected_result": {"type": ValueError,
                                     "message": "Column: {\"name\": \"X\", \"type\": \"invalid_type\"}, type is invalid. Type must be one of the following: " + ", ".join(
                                         valid_types)}
                 },
                {"data": {"columns": [{"type": "boolean"}]},
                 "expected_result": {"type": ValueError,
                                     "message": "Column: {\"type\": \"boolean\"}, is missing either 'name' or 'type' fields"}
                 },
                {"data": {"columns": [{"name": "", "type": "boolean"}]},
                 "expected_result": {"type": ValueError,
                                     "message": "Column: {\"name\": \"\", \"type\": \"boolean\"}, Can't have empty or none string name value"}
                 },
                {"data": {"columns": [{"name": 1, "type": "boolean"}]},
                 "expected_result": {"type": ValueError,
                                     "message": "Column: {\"name\": 1, \"type\": \"boolean\"}, Can't have empty or none string name value"}
                 },
            ]
        }

    @patch('uuid.uuid4')
    def test_valid_json_input(self, mock_uuid):
        mock_uuid.return_value = fixed_uuid()

        for valid_json in self.test_data["valid"]:
            self.assertEqual(create_new_sheet(valid_json["data"]), valid_json["expected_result"])

    def test_invalid_json_inputs(self):
        for invalid_json in self.test_data["invalid"]:
            with self.assertRaises(invalid_json["expected_result"]["type"]) as e:
                self.assertEqual(create_new_sheet(invalid_json["data"]),
                                 invalid_json["expected_result"]["message"])
