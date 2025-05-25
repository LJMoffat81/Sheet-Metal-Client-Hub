import unittest
import sys
import os
import tempfile
from unittest.mock import patch

# Add src/ to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from file_handler import validate_credentials, load_rates, save_output, save_quote, update_rates, BASE_DIR

class TestFileHandler(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.users_file = os.path.join(self.temp_dir, 'users.txt')
        self.rates_file = os.path.join(self.temp_dir, 'rates_global.txt')
        self.output_file = os.path.join(self.temp_dir, 'output.txt')
        self.quotes_file = os.path.join(self.temp_dir, 'quotes.txt')

        # Create test users file
        with open(self.users_file, 'w', encoding='utf-8') as f:
            f.write('laurie:moffat123\n')

        # Create test rates file
        with open(self.rates_file, 'w', encoding='utf-8') as f:
            f.write('mild_steel_rate=0.10\nwelding_rate_per_mm=0.10\n')

        # Mock BASE_DIR to use temp_dir
        self.original_base_dir = BASE_DIR
        with patch('file_handler.BASE_DIR', self.temp_dir):
            self.temp_dir_patched = True

    def tearDown(self):
        # No need to restore BASE_DIR since patch is scoped to setUp
        pass

    def test_validate_credentials_valid(self):
        result = validate_credentials('laurie', 'moffat123')
        self.assertTrue(result, "Valid credentials should return True")

    def test_validate_credentials_invalid(self):
        result = validate_credentials('laurie', 'wrong')
        self.assertFalse(result, "Invalid credentials should return False")

    def test_load_rates(self):
        rates = load_rates()
        self.assertIn('mild_steel_rate', rates, "Rates should include mild_steel_rate")
        self.assertEqual(rates['mild_steel_rate'], 0.10, "Rate should match file value")

    def test_save_output(self):
        save_output('PART-12345', '1', 'mild steel', 1.0, 1000, 500, 1, 50.0)
        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        self.assertEqual(content, "PART-12345,1,mild steel,1.0,1000,500,1,50.0", "Output should be saved correctly")

    def test_save_quote(self):
        save_quote('PART-12345', 50.0, 'Acme', 20.0)
        with open(self.quotes_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        self.assertEqual(content, "PART-12345,Acme,50.0,20.0", "Quote should be saved correctly")

    def test_update_rates(self):
        update_rates('mild_steel_rate', 0.15)
        rates = load_rates()
        self.assertEqual(rates['mild_steel_rate'], 0.15, "Rate should be updated")

if __name__ == '__main__':
    unittest.main()
