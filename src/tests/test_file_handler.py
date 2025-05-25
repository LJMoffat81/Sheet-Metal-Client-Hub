import unittest
import sys
import os
import tempfile
from unittest.mock import patch

# Add src/ to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from file_handler import validate_credentials, load_rates, save_output, save_quote, update_rates

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

    @patch('file_handler.os.path.join')
    def test_validate_credentials_valid(self, mock_join):
        mock_join.side_effect = lambda *args: os.path.join(self.temp_dir, args[-1])
        result = validate_credentials('laurie', 'moffat123')
        self.assertTrue(result, "Valid credentials should return True")

    @patch('file_handler.os.path.join')
    def test_validate_credentials_invalid(self, mock_join):
        mock_join.side_effect = lambda *args: os.path.join(self.temp_dir, args[-1])
        result = validate_credentials('laurie', 'wrong')
        self.assertFalse(result, "Invalid credentials should return False")

    @patch('file_handler.os.path.join')
    def test_load_rates(self, mock_join):
        mock_join.side_effect = lambda *args: os.path.join(self.temp_dir, args[-1])
        rates = load_rates()
        self.assertIn('mild_steel_rate', rates, "Rates should include mild_steel_rate")
        self.assertEqual(rates['mild_steel_rate'], 0.10, "Rate should match file value")

    @patch('file_handler.os.path.join')
    def test_save_output(self, mock_join):
        mock_join.side_effect = lambda *args: os.path.join(self.temp_dir, args[-1])
        save_output('PART-12345', '1', 'mild steel', 1.0, 1000, 500, 1, 50.0)
        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        self.assertEqual(content, "PART-12345,1,mild steel,1.0,1000,500,1,50.0", "Output should be saved correctly")

    @patch('file_handler.os.path.join')
    def test_save_quote(self, mock_join):
        mock_join.side_effect = lambda *args: os.path.join(self.temp_dir, args[-1])
        save_quote('PART-12345', 50.0, 'Acme', 20.0)
        with open(self.quotes_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        self.assertEqual(content, "PART-12345,Acme,50.0,20.0", "Quote should be saved correctly")

    @patch('file_handler.os.path.join')
    def test_update_rates(self, mock_join):
        mock_join.side_effect = lambda *args: os.path.join(self.temp_dir, args[-1])
        update_rates('mild_steel_rate', 0.15)
        rates = load_rates()
        self.assertEqual(rates['mild_steel_rate'], 0.15, "Rate should be updated")

if __name__ == '__main__':
    unittest.main()
