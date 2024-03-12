import unittest
from spreadsheet_app.spreadsheet import get_spreadsheet_values


class GetSpreadsheetValuesTest(unittest.TestCase):
    def test_valid_json_input(self):
        expected_output = {"('BOOLEAN', 0)": True,
                           "('INT', 0)": 1, 
                           "('DOUBLE', 0)": 1.0, 
                           "('STRING', 0)": 'string', 
                           "('BOOLEAN', 1)": True, 
                           "('BOOLEAN', 2)": True}
        self.assertEqual(get_spreadsheet_values('mock'), expected_output)
