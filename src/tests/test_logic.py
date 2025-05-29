import unittest
from unittest.mock import patch, MagicMock
from logic import calculate_and_save

class TestLogic(unittest.TestCase):
    @patch('file_handler.FileHandler')
    def test_calculate_and_save(self, mock_file_handler):
        mock_rates = {
            "mild_steel_rate": {"value": 1500},
            "cutting_rate": {"value": 0.003, "type": "simple"}
        }
        mock_file_handler.return_value.load_rates.return_value = mock_rates
        mock_file_handler.return_value.save_output = MagicMock()
        part_specs = {
            "part_type": "Single Part",
            "part_id": "PART-12345",
            "revision": "A",
            "specs": {
                "material": "Mild Steel",
                "thickness": 1.0,
                "length": 1000,
                "width": 500,
                "quantity": 1,
                "sub_parts": [],
                "fastener_types_and_counts": [],
                "top_level_assembly": False,
                "weldment_indicator": False
            },
            "work_centres": [("Cutting", 100, "None")]
        }
        result = calculate_and_save(part_specs, mock_file_handler, mock_rates, [], lambda x, y, z: None)
        self.assertIsInstance(result, float)