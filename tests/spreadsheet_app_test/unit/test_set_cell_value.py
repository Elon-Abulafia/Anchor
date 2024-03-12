import unittest
from spreadsheet_app.spreadsheet import set_cell_value
from tests.consts import VALID_VALUES, COLUMN_NAMES
from tests.spreadsheet_app_test.unit.test_create_new_sheet import fixed_uuid


class SetCellValueTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_data = {"valid": [], "invalid": []}

        for col_name in COLUMN_NAMES:
            self.test_data["valid"].append(
                {
                    "data":
                        {
                            "sheet_id": fixed_uuid(),
                            "column_name": col_name,
                            "cell_index": 0,
                            "value": VALID_VALUES[col_name],
                        },
                    "expected_result": None
                }
            )
            self.test_data["invalid"].append(
                {
                    "data":
                        {
                            "sheet_id": fixed_uuid(),
                            "column_name": col_name,
                            "cell_index": 1,
                            "value": None,
                        },
                    "expected_result": {"type": TypeError, "message": "Cell value type must match column type"}
                }
            )
        self.insert_valid_lookup_functions()
        self.insert_invalid_lookup_functions()

    def insert_invalid_lookup_functions(self):
        self.test_data["invalid"].append(
            {
                "data":
                    {
                        "sheet_id": fixed_uuid(),
                        "column_name": COLUMN_NAMES[0],
                        "cell_index": 0,
                        "value": f"lookup({COLUMN_NAMES[0]}, 0)",
                    },
                "expected_result": {"type": LookupError,
                                    "message": "Encountered infinite loop or invalid type while trying to insert new lookup expression"}
            }
        )
        self.test_data["invalid"].append(
            {
                "data":
                    {
                        "sheet_id": fixed_uuid(),
                        "column_name": COLUMN_NAMES[0],
                        "cell_index": 0,
                        "value": f"lookup({COLUMN_NAMES[1]}, 0)",
                    },
                "expected_result": {"type": LookupError,
                                    "message": "Encountered infinite loop or invalid type while trying to insert new lookup expression"}
            }
        )

    def insert_valid_lookup_functions(self):
        self.test_data["valid"].append(
            {
                "data":
                    {
                        "sheet_id": fixed_uuid(),
                        "column_name": COLUMN_NAMES[0],
                        "cell_index": 1,
                        "value": f"lookup({COLUMN_NAMES[0]}, 0)",
                    },
                "expected_result": None
            }
        )
        self.test_data["valid"].append(
            {
                "data":
                    {
                        "sheet_id": fixed_uuid(),
                        "column_name": COLUMN_NAMES[0],
                        "cell_index": 2,
                        "value": f"lookup({COLUMN_NAMES[0]}, 1)",
                    },
                "expected_result": None
            }
        )

    def test_valid_input(self):
        for valid_input in self.test_data["valid"]:
            self.assertIsNone(set_cell_value(**valid_input["data"]))

    def test_invalid_inputs(self):
        for invalid_input in self.test_data["invalid"]:
            with self.assertRaises(invalid_input["expected_result"]["type"]) as e:
                self.assertEqual(set_cell_value(**invalid_input["data"]),
                                 invalid_input["expected_result"]["message"])
