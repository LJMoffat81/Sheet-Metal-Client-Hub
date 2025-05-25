import unittest
import os
from file_handler import FileHandler  # Import the class
from calculator import calculate_cost

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.file_handler = FileHandler()  # Create an instance
        self.rates = self.file_handler.load_rates('rates_global.txt')  # Use instance method

    def test_calculate_cost_single_part(self):
        part_specs = {
            'part_type': 'Single Part',
            'part_id': 'PART-12345',
            'revision': '1',
            'material': 'mild steel',
            'thickness': 1.0,
            'length': 1000,
            'width': 500,
            'quantity': 1,
            'sub_parts': ['FAS-001: Screw M3'],
            'weldment_indicator': 'No',
            'top_level_assembly': 'N/A',
            'catalogue_cost': 0.50,
            'work_centres': [('Welding', 500.0)]
        }
        cost = calculate_cost(part_specs, self.rates)
        self.assertGreater(cost, 0.0, "Cost should be positive for valid inputs")

if __name__ == '__main__':
    unittest.main()
