# test_calculator.py
# Purpose: Unit tests for the calculator module to verify cost calculation functionality (FR3-FR4).
# Tests the calculate_cost function to ensure accurate cost computations based on part specifications.
# Uses unittest framework for automated testing, suitable for college project evaluation.
# Logs test results to test_logs.txt using logger.py.

import unittest
from ..calculator import calculate_cost
from ..logger import log_test_result

class TestCalculator(unittest.TestCase):
    """
    Test case class for calculator.py, focusing on cost calculation (FR3-FR4).
    """
    def setUp(self):
        """
        Set up sample rates for tests, mimicking rates_global.txt.
        
        Logic:
            1. Defines a rates dictionary with material, labour, and process rates.
        """
        self.rates = {
            'steel_rate': 5.0,
            'aluminum_rate': 7.0,
            'labour_rate': 20.0,
            'laser_cutting': 25.0,
            'bending': 15.0,
            'welding': 30.0,
            'painting': 10.0,
            'assembly': 12.0,
            'inspection': 8.0,
            'packaging': 5.0,
            'turret_press': 20.0
        }

    def test_calculate_cost_valid_steel(self):
        """
        Test calculate_cost with a valid steel part specification (FR3-FR4).
        
        Logic:
            1. Calls calculate_cost with a steel part (2 mm thick, 1000x500 mm, 100 units).
            2. Calculates expected cost.
            3. Asserts calculated cost matches expected cost.
            4. Logs test result to test_logs.txt.
        """
        input_data = "Part ID: PART-123, Revision: Rev A1, Material: steel, Thickness: 2.0, Length: 1000, Width: 500, Quantity: 100"
        try:
            part_specs = {
                'part_type': 'Single Part',
                'part_id': 'PART-123',
                'revision': 'Rev A1',
                'material': 'steel',
                'thickness': 2.0,
                'length': 1000,
                'width': 500,
                'quantity': 100,
                'cutting_method': 'None',
                'cutting_complexity': 0
            }
            cost = calculate_cost(part_specs, self.rates)
            expected = (2.0 * 1000 * 500 * 5.0 * 100) + (2.0 * 1000 * 500 * 20.0 * 100)
            self.assertAlmostEqual(cost, expected, places=2)
            log_test_result(
                test_case="FR3-FR4: Valid steel cost calculation",
                input_data=input_data,
                output=f"Calculated cost: £{cost}, Expected: £{expected}",
                pass_fail="Pass"
            )
        except AssertionError as e:
            log_test_result(
                test_case="FR3-FR4: Valid steel cost calculation",
                input_data=input_data,
                output=f"AssertionError: {e}",
                pass_fail="Fail"
            )
            raise

    def test_calculate_cost_invalid_material(self):
        """
        Test calculate_cost with an invalid material (FR3-FR4).
        
        Logic:
            1. Calls calculate_cost with an invalid material (e.g., "copper").
            2. Asserts cost is 0.0.
            3. Logs test result to test_logs.txt.
        """
        input_data = "Part ID: PART-123, Revision: Rev A1, Material: copper, Thickness: 2.0, Length: 1000, Width: 500, Quantity: 100"
        try:
            part_specs = {
                'part_type': 'Single Part',
                'part_id': 'PART-123',
                'revision': 'Rev A1',
                'material': 'copper',
                'thickness': 2.0,
                'length': 1000,
                'width': 500,
                'quantity': 100,
                'cutting_method': 'None',
                'cutting_complexity': 0
            }
            cost = calculate_cost(part_specs, self.rates)
            self.assertEqual(cost, 0.0)
            log_test_result(
                test_case="FR3-FR4: Invalid material",
                input_data=input_data,
                output="Cost: 0.0 (as expected)",
                pass_fail="Pass"
            )
        except AssertionError as e:
            log_test_result(
                test_case="FR3-FR4: Invalid material",
                input_data=input_data,
                output=f"AssertionError: {e}",
                pass_fail="Fail"
            )
            raise

    def test_calculate_cost_invalid_thickness(self):
        """
        Test calculate_cost with an invalid thickness (FR3-FR4).
        
        Logic:
            1. Calls calculate_cost with a thickness outside 1-3 mm (e.g., 4.0 mm).
            2. Asserts cost is 0.0.
            3. Logs test result to test_logs.txt.
        """
        input_data = "Part ID: PART-123, Revision: Rev A1, Material: steel, Thickness: 4.0, Length: 1000, Width: 500, Quantity: 100"
        try:
            part_specs = {
                'part_type': 'Single Part',
                'part_id': 'PART-123',
                'revision': 'Rev A1',
                'material': 'steel',
                'thickness': 4.0,
                'length': 1000,
                'width': 500,
                'quantity': 100,
                'cutting_method': 'None',
                'cutting_complexity': 0
            }
            cost = calculate_cost(part_specs, self.rates)
            self.assertEqual(cost, 0.0)
            log_test_result(
                test_case="FR3-FR4: Invalid thickness",
                input_data=input_data,
                output="Cost: 0.0 (as expected)",
                pass_fail="Pass"
            )
        except AssertionError as e:
            log_test_result(
                test_case="FR3-FR4: Invalid thickness",
                input_data=input_data,
                output=f"AssertionError: {e}",
                pass_fail="Fail"
            )
            raise

    def test_calculate_cost_assembly(self):
        """
        Test calculate_cost with an assembly containing sub-parts (FR3-FR4).
        
        Logic:
            1. Defines an assembly with two sub-parts.
            2. Calculates expected cost.
            3. Asserts calculated cost matches expected.
            4. Logs test result.
        """
        input_data = "Assembly with 2 sub-parts, 2 assembly components"
        part_specs = {
            'part_type': 'Assembly',
            'material': 'steel',
            'thickness': 2.0,
            'length': 100,
            'width': 50,
            'quantity': 1,
            'sub_parts': [
                {'part_type': 'Single Part', 'material': 'steel', 'thickness': 2.0, 'length': 100, 'width': 50, 'quantity': 1, 'cutting_method': 'None', 'cutting_complexity': 0},
                {'part_type': 'Single Part', 'material': 'aluminum', 'thickness': 1.0, 'length': 200, 'width': 100, 'quantity': 1, 'cutting_method': 'Laser Cutting', 'cutting_complexity': 5}
            ],
            'assembly_components': 2
        }
        try:
            cost = calculate_cost(part_specs, self.rates)
            expected = ((2.0 * 100 * 50 * 5.0 + 2.0 * 100 * 50 * 20.0) +  # First sub-part
                        (1.0 * 200 * 100 * 7.0 + 1.0 * 200 * 100 * 20.0 + 25.0 * 5) +  # Second sub-part
                        (12.0 * 2))  # Assembly cost
            self.assertAlmostEqual(cost, expected, places=2)
            log_test_result(
                test_case="FR3-FR4: Assembly cost calculation",
                input_data=input_data,
                output=f"Calculated cost: £{cost}, Expected: £{expected}",
                pass_fail="Pass"
            )
        except AssertionError as e:
            log_test_result(
                test_case="FR3-FR4: Assembly cost calculation",
                input_data=input_data,
                output=f"AssertionError: {e}",
                pass_fail="Fail"
            )
            raise

if __name__ == '__main__':
    unittest.main()
