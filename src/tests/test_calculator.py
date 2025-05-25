import unittest
from unittest.mock import patch
from file_handler import FileHandler
from calculator import calculate_cost
import logging
import os

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.file_handler = FileHandler()
        self.rates = self.file_handler.load_rates()
        self.log_file = os.path.join('data', 'log', 'calculator.log')
        logging.basicConfig(
            filename=self.log_file,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def test_calculate_cost_single_part(self):
        part_data = {
            'part_type': 'Single Part',
            'material': 'mild_steel',
            'thickness': 1.0,
            'length': 1000,
            'width': 500,
            'quantity': 1,
            'work_centres': [('Cutting', 3000), ('Bending', 2)],
            'catalogue_cost': 1.0
        }
        cost = calculate_cost(part_data, self.rates)
        self.assertAlmostEqual(cost, 51.0, places=2)
        with open(self.log_file, 'r') as f:
            log_content = f.read()
            self.assertIn(f"Calculated cost: {cost}", log_content)

    def test_calculate_cost_assembly(self):
        part_data = {
            'part_type': 'Assembly',
            'material': 'N/A',
            'thickness': 0.0,
            'length': 0,
            'width': 0,
            'quantity': 10,
            'work_centres': [('Assembly', 10)],
            'catalogue_cost': 0.0
        }
        cost = calculate_cost(part_data, self.rates)
        self.assertAlmostEqual(cost, 8.0, places=2)
        with open(self.log_file, 'r') as f:
            log_content = f.read()
            self.assertIn(f"Calculated cost: {cost}", log_content)

    def test_calculate_cost_invalid_work_centre(self):
        part_data = {
            'part_type': 'Single Part',
            'material': 'mild_steel',
            'thickness': 1.0,
            'length': 1000,
            'width': 500,
            'quantity': 1,
            'work_centres': [('Invalid', 100)],
            'catalogue_cost': 0.0
        }
        cost = calculate_cost(part_data, self.rates)
        self.assertEqual(cost, 0.0)
        with open(self.log_file, 'r') as f:
            log_content = f.read()
            self.assertIn("Missing rate", log_content)

    def test_calculate_cost_missing_rate(self):
        part_data = {
            'part_type': 'Single Part',
            'material': 'invalid_material',
            'thickness': 1.0,
            'length': 1000,
            'width': 500,
            'quantity': 1,
            'work_centres': [('Cutting', 100)],
            'catalogue_cost': 0.0
        }
        cost = calculate_cost(part_data, self.rates)
        self.assertEqual(cost, 0.0)
        with open(self.log_file, 'r') as f:
            log_content = f.read()
            self.assertIn("Missing rate", log_content)

if __name__ == '__main__':
    unittest.main()
