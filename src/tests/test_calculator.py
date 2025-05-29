import unittest
from calculator import calculate_cost

class TestCalculator(unittest.TestCase):
    def test_cost_mild_steel(self):
        mock_rates = {
            "mild_steel_rate": {"value": 1500},
            "cutting_rate": {"value": 0.003, "type": "simple"}
        }
        part_specs = {
            "part_id": "PART-101",
            "part_type": "Single Part",
            "material": "mild_steel_rate",
            "thickness": 1.0,
            "length": 1000,
            "width": 500,
            "quantity": 1,
            "work_centres": [("Cutting", 100, "None")]
        }
        result = calculate_cost(part_specs, mock_rates)
        self.assertAlmostEqual(result, 750.3, places=2)