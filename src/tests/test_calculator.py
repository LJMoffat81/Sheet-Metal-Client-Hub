import unittest
from unittest.mock import patch
from file_handler import FileHandler
from calculator import calculate_cost
import logging
import os

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.file_handler = FileHandler()
        self.rates = {
            'mild_steel_rate': 0.0001,
            'cutting_rate_per_mm': 0.01,
            'bending_rate_per_bend': 0.5,
            'mig_welding_rate_per_mm': 0.02,
            'painting_rate_per_mm²': 0.001,
            'bolts_rate_per_unit': 0.1,
            'assembly_rate_per_component': 0.8
        }
        self.log_file = os.path.join('data', 'log', 'calculator.log')
        logging.basicConfig(
            filename=self.log_file,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def test_calculate_cost_single_part_with_welding(self):
        part_data = {
            'part_type': 'Single Part',
            'material': 'mild_steel',
            'thickness': 1.0,
            'length': 1000,
            'width': 500,
            'quantity': 10,
            'work_centres': [('Welding', 100, 'MIG')],
            'catalogue_cost': 0.0,
            'fastener_types_and_counts': []
        }
        cost = calculate_cost(part_data, self.rates)
        expected_cost = 0.0001 * 1.0 * 1000 * 500 * 10 + 0.02 * 100 * 10  # Material + Welding
        self.assertAlmostEqual(cost, expected_cost, places=2)
        with open(self.log_file, 'r') as f:
            log_content = f.read()
            self.assertIn(f"Calculated cost: {cost}", log_content)

    def test_calculate_cost_single_part_with_coating(self):
        part_data = {
            'part_type': 'Single Part',
            'material': 'mild_steel',
            'thickness': 1.0,
            'length': 1000,
            'width': 500,
            'quantity': 5,
            'work_centres': [('Coating', 1000, 'Painting')],
            'catalogue_cost': 0.0,
            'fastener_types_and_counts': []
        }
        cost = calculate_cost(part_data, self.rates)
        expected_cost = 0.0001 * 1.0 * 1000 * 500 * 5 + 0.001 * 1000 * 5  # Material + Coating
        self.assertAlmostEqual(cost, expected_cost, places=2)
        with open(self.log_file, 'r') as f:
            log_content = f.read()
            self.assertIn(f"Calculated cost: {cost}", log_content)

    def test_calculate_cost_single_part_with_fasteners(self):
        part_data = {
            'part_type': 'Single Part',
            'material': 'mild_steel',
            'thickness': 1.0,
            'length': 1000,
            'width': 500,
            'quantity': 2,
            'work_centres': [('Cutting', 3000, 'None')],
            'catalogue_cost': 1.0,
            'fastener_types_and_counts': [('Bolts', 50)]
        }
        cost = calculate_cost(part_data, self.rates)
        expected_cost = (0.0001 * 1.0 * 1000 * 500 * 2) + (0.01 * 3000 * 2) + (0.1 * 50 * 2) + (1.0 * 2)  # Material + Cutting + Bolts + Catalogue
        self.assertAlmostEqual(cost, expected_cost, places=2)
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
            'work_centres': [('Assembly', 10, 'None')],
            'catalogue_cost': 0.0,
            'fastener_types_and_counts': []
        }
        cost = calculate_cost(part_data, self.rates)
        expected_cost = 0.8 * 10 * 10  # Assembly components
        self.assertAlmostEqual(cost, expected_cost, places=2)
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
            'work_centres': [('Invalid', 100, 'None')],
            'catalogue_cost': 0.0,
            'fastener_types_and_counts': []
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
            'work_centres': [('Cutting', 100, 'None')],
            'catalogue_cost': 0.0,
            'fastener_types_and_counts': []
        }
        cost = calculate_cost(part_data, self.rates)
        self.assertEqual(cost, 0.0)
        with open(self.log_file, 'r') as f:
            log_content = f.read()
            self.assertIn("Missing rate", log_content)

if __name__ == '__main__':
    unittest.main()