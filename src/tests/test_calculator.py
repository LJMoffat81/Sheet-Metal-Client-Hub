# test_calculator.py
# Purpose: Unit tests for the calculator module to verify cost calculation functionality (FR3-FR4).
# Tests the calculate_cost function to ensure accurate cost computations based on part specifications.
# Uses unittest framework for automated testing, suitable for college project evaluation.
# Tests cover typical use cases with steel material and predefined rates.

import unittest
from calculator import calculate_cost

class TestCalculator(unittest.TestCase):
    """
    Test case class for calculator.py, focusing on cost calculation (FR3-FR4).
    """
    def test_calculate_cost(self):
        """
        Test calculate_cost with a typical part specification (FR3-FR4).
        
        Logic:
            1. Defines a sample rates dictionary mimicking rates_global.txt.
            2. Calls calculate_cost with a steel part (2 mm thick, 1000x500 mm, 100 units).
            3. Calculates expected cost: 
               - Material cost: volume (2 * 1000 * 500) * steel_rate (5.0) * quantity (100)
               - Labour cost: volume * labour_rate (20.0) * quantity
               - Process cost: sum of process rates * quantity
            4. Asserts calculated cost matches expected cost within 2 decimal places.
        """
        rates = {
            'steel_rate': 5.0,
            'labour_rate': 20.0,
            'laser_cutting': 25.0,
            'bending': 15.0,
            'welding': 30.0,
            'painting': 10.0,
            'assembly': 12.0,
            'inspection': 8.0,
            'packaging': 5.0
        }
        cost = calculate_cost("PART-123", "Rev A1", "steel", 2.0, 1000, 500, 100, rates)
        expected = (2.0 * 1000 * 500 * 5.0 * 100) + (2.0 * 1000 * 500 * 20.0 * 100) + (25.0 + 15.0 + 30.0 + 10.0 + 12.0 + 8.0 + 5.0) * 100
        self.assertAlmostEqual(cost, expected, places=2)

if __name__ == '__main__':
    unittest.main()
