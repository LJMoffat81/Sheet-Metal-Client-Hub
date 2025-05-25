import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from gui import SheetMetalGUI
from file_handler import FileHandler

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = SheetMetalGUI(self.root)
        self.file_handler = FileHandler()

    def tearDown(self):
        self.root.destroy()

    @patch('gui.FileHandler.validate_credentials')
    def test_login_success(self, mock_validate):
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'laurie')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.assertIsNotNone(self.app.part_input_frame)

    def test_login_invalid(self):
        self.app.username_entry.insert(0, 'wrong')
        self.app.password_entry.insert(0, 'wrong')
        with self.assertLogs(level='WARNING') as cm:
            self.app.login()
            self.assertIn('Invalid credentials', cm.output[0])

    def test_login_empty_fields(self):
        with self.assertLogs(level='WARNING') as cm:
            self.app.login()
            self.assertIn('Username and password cannot be empty', cm.output[0])

    def test_part_input_screen(self):
        self.app.show_part_input_screen()
        self.assertIsNotNone(self.app.part_input_frame)
        self.assertEqual(self.app.part_input_frame.winfo_exists(), 1)

    def test_part_input_invalid_dimensions(self):
        self.app.show_part_input_screen()
        self.app.length_entry.insert(0, '-100')
        with self.assertLogs(level='ERROR') as cm:
            self.app.submit_part()
            self.assertIn('Invalid dimensions', cm.output[0])

    def test_part_input_assembly(self):
        self.app.show_part_input_screen()
        self.app.part_type_var.set('Assembly')
        self.app.quantity_entry.insert(0, '10')
        self.app.submit_part()
        self.assertIsNotNone(self.app.cost_display)

    @patch('gui.FileHandler.update_rates')
    def test_update_rate_valid(self, mock_update):
        self.app.show_rate_update_screen()
        self.app.rate_key_var.set('mild_steel_rate')
        self.app.rate_value_entry.insert(0, '0.3')
        self.app.update_rate()
        mock_update.assert_called_with('mild_steel_rate', '0.3')

    def test_update_rate_invalid(self):
        self.app.show_rate_update_screen()
        self.app.rate_key_var.set('mild_steel_rate')
        self.app.rate_value_entry.insert(0, 'invalid')
        with self.assertLogs(level='ERROR') as cm:
            self.app.update_rate()
            self.assertIn('Invalid rate value', cm.output[0])

    @patch('gui.FileHandler.save_quote')
    def test_generate_quote_valid(self, mock_save_quote):
        self.app.cost = 100.0
        self.app.part_id = 'PART-123'
        self.app.show_quote_screen()
        self.app.customer_entry.insert(0, 'Acme Corp')
        self.app.margin_entry.insert(0, '20')
        self.app.generate_quote()
        mock_save_quote.assert_called()

    def test_generate_quote_invalid_margin(self):
        self.app.cost = 100.0
        self.app.part_id = 'PART-123'
        self.app.show_quote_screen()
        self.app.customer_entry.insert(0, 'Acme Corp')
        self.app.margin_entry.insert(0, '-10')
        with self.assertLogs(level='ERROR') as cm:
            self.app.generate_quote()
            self.assertIn('Invalid margin', cm.output[0])

if __name__ == '__main__':
    unittest.main()
