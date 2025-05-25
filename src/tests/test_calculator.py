import unittest
import sys
import os

# Add src/ to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from calculator import calculate_cost
from file_handler import load_rates

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.rates = load_rates()

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

    def test_calculate_cost_assembly(self):
        part_specs = {
            'part_type': 'Assembly',
            'part_id': 'ASSY-67890',
            'revision': '2',
            'material': 'N/A',
            'thickness': 0.0,
            'length': 0,
            'width': 0,
            'quantity': 10,
            'sub_parts': ['PART-12345'],
            'weldment_indicator': 'No',
            'top_level_assembly': 'ASSY-67890',
            'catalogue_cost': 0.0,
            'work_centres': [('Assembly', 5.0)]
        }
        cost = calculate_cost(part_specs, self.rates)
        self.assertGreater(cost, 0.0, "Cost should be positive for valid assembly")

    def test_calculate_cost_missing_rate(self):
        part_specs = {
            'part_type': 'Single Part',
            'part_id': 'PART-54321',
            'revision': '1',
            'material': 'invalid_material',
            'thickness': 1.0,
            'length': 1000,
            'width': 500,
            'quantity': 1,
            'sub_parts': [],
            'weldment_indicator': 'No',
            'top_level_assembly': 'N/A',
            'catalogue_cost': 0.0,
            'work_centres': [('Welding', 500.0)]
        }
        cost = calculate_cost(part_specs, self.rates)
        self.assertEqual(cost, 0.0, "Cost should be 0.0 for missing material rate")

    def test_calculate_cost_invalid_work_centre(self):
        part_specs = {
            'part_type': 'Single Part',
            'part_id': 'PART-12345',
            'revision': '1',
            'material': 'mild steel',
            'thickness': 1.0,
            'length': 1000,
            'width': 500,
            'quantity': 1,
            'sub_parts': [],
            'weldment_indicator': 'No',
            'top_level_assembly': 'N/A',
            'catalogue_cost': 0.0,
            'work_centres': [('InvalidCentre', 500.0)]
        }
        cost = calculate_cost(part_specs, self.rates)
        self.assertEqual(cost, 0.0, "Cost should be 0.0 for invalid work centre")

if __name__ == '__main__':
    unittest.main()
