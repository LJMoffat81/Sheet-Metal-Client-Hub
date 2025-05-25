import unittest
from unittest.mock import patch
from file_handler import FileHandler
from calculator import calculate_cost

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.file_handler = FileHandler()
        self.rates = self.file_handler.load_rates()

    def test_calculate_cost_single_part(self):
        part_data = {
            'part_type': 'Part',
            'material': 'mild_steel',
            'thickness': 1.0,
            'length': 1000,
            'width': 500,
            'quantity': 1,
            'work_centres': ['cutting', 'bending']
        }
        cost = calculate_cost(part_data, self.rates)
        self.assertAlmostEqual(cost, 50.0, places=2)

    def test_calculate_cost_assembly(self):
        part_data = {
            'part_type': 'Assembly',
            'material': 'N/A',
            'thickness': 0.0,
            'length': 0,
            'width': 0,
            'quantity': 10,
            'components': 10,
            'work_centres': ['assembly']
        }
        cost = calculate_cost(part_data, self.rates)
        self.assertAlmostEqual(cost, 8.0, places=2)

    def test_calculate_cost_invalid_work_centre(self):
        part_data = {
            'part_type': 'Part',
            'material': 'mild_steel',
            'thickness': 1.0,
            'length': 1000,
            'width': 500,
            'quantity': 1,
            'work_centres': ['invalid']
        }
        with self.assertLogs(level='ERROR') as cm:
            cost = calculate_cost(part_data, self.rates)
            self.assertEqual(cost, 0.0)
            self.assertTrue(any("Missing rate" in msg for msg in cm.output))

    def test_calculate_cost_missing_rate(self):
        part_data = {
            'part_type': 'Part',
            'material': 'invalid_material',
            'thickness': 1.0,
            'length': 1000,
            'width': 500,
            'quantity': 1,
            'work_centres': ['cutting']
        }
        with self.assertLogs(level='ERROR') as cm:
            cost = calculate_cost(part_data, self.rates)
            self.assertEqual(cost, 0.0)
            self.assertTrue(any("Missing rate" in msg for msg in cm.output))

if __name__ == '__main__':
    unittest.main()
