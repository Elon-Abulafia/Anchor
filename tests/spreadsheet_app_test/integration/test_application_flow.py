import json
import unittest
from unittest.mock import patch
from spreadsheet_app import app


class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        with open("D:\\Users\\Elon\\PycharmProjects\\Anchor\\tests\\spreadsheet_app_test\\integration\\base_config_json.json", "r") as f:
            self.json_schema = json.load(f)

    @patch('uuid.uuid4')
    def test_get_user(self, mock_uuid):
        expected_sheet_id = "fixed-integration-uuid"
        expected_final_sheet = {
            "('BOOLEAN', 0)": True,
            "('BOOLEAN', 1)": True,
            "('INT', 0)": 0,
            "('STRING', 0)": 'string'
        }
        mock_uuid.return_value = expected_sheet_id

        response = self.client.post('/sheet', json=self.json_schema)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.text, expected_sheet_id)

        response = self.client.put('/sheet', json={
            "sheet_id": expected_sheet_id,
            "column_name": "BOOLEAN",
            "cell_index": 0,
            "value": True,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Cell value set successfully")

        response = self.client.put('/sheet', json={
            "sheet_id": expected_sheet_id,
            "column_name": "STRING",
            "cell_index": 0,
            "value": "string",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Cell value set successfully")

        response = self.client.put('/sheet', json={
            "sheet_id": expected_sheet_id,
            "column_name": "INT",
            "cell_index": 0,
            "value": 0,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Cell value set successfully")

        response = self.client.put('/sheet', json={
            "sheet_id": expected_sheet_id,
            "column_name": "BOOLEAN",
            "cell_index": 1,
            "value": "lookup(BOOLEAN, 0)",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Cell value set successfully")

        response = self.client.get(f"/sheet/{expected_sheet_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.get_json(), expected_final_sheet)
