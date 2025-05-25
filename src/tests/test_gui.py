import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from gui import SheetMetalClientHub
from file_handler import FileHandler

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = SheetMetalClientHub(self.root)
        self.file_handler = FileHandler()

    def tearDown(self):
        self.root.destroy()

    @patch('gui.FileHandler.validate_credentials')
    def test_login_success_user(self, mock_validate):
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'laurie')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.assertIsNotNone(self.app.notebook)

    @patch('gui.FileHandler.validate_credentials')
    def test_login_success_admin(self, mock_validate):
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'admin')
        self.app.password_entry.insert(0, 'admin123')
        self.app.login()
        self.assertIsNotNone(self.app.rate_key_entry)

    def test_login_invalid(self):
        self.app.username_entry.insert(0, 'wrong')
        self.app.password_entry.insert(0, 'wrong')
        with self.assertLogs(level='INFO') as cm:
            self.app.login()
            self.assertIn('Invalid credentials', cm.output[0])

    def test_login_empty_fields(self):
        with self.assertLogs(level='INFO') as cm:
            self.app.login()
            self.assertIn('Username and password cannot be empty', cm.output[0])

    def test_part_input_screen(self):
        self.app.create_part_input_screen()
        self.assertIsNotNone(self.app.notebook)
        self.assertEqual(self.app.notebook.winfo_exists(), 1)

    def test_part_input_invalid_dimensions(self):
        self.app.create_part_input_screen()
        self.app.notebook.select(1)  # Single Part tab
        self.app.single_lay_flat_length_var.set('-100')
        with self.assertLogs(level='INFO') as cm:
            self.app.calculate_and_save()
            self.assertIn('Lay-Flat length must be between 50 and 3000 mm', cm.output[0])

    def test_part_input_assembly_no_sub_parts(self):
        self.app.create_part_input_screen()
        self.app.notebook.select(0)  # Assembly tab
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'ASSY-12345')
        self.app.revision_entry.insert(0, 'A')
        self.app.assembly_quantity_var.set('10')
        with self.assertLogs(level='INFO') as cm:
            self.app.calculate_and_save()
            self.assertIn('At least one sub-part must be selected for an assembly', cm.output[0])

    @patch('gui.FileHandler.update_rates')
    def test_update_rate_valid(self, mock_update):
        self.app.create_admin_screen()
        self.app.rate_key_entry.insert(0, 'mild_steel_rate')
        self.app.rate_value_entry.insert(0, '0.3')
        self.app.update_rate()
        mock_update.assert_called_with('mild_steel_rate', 0.3)

    def test_update_rate_invalid(self):
        self.app.create_admin_screen()
        self.app.rate_key_entry.insert(0, 'mild_steel_rate')
        self.app.rate_value_entry.insert(0, 'invalid')
        with self.assertLogs(level='INFO') as cm:
            self.app.update_rate()
            self.assertIn('Invalid rate value', cm.output[0])

    @patch('gui.FileHandler.save_quote')
    def test_generate_quote_valid(self, mock_save_quote):
        self.app.create_quote_screen('PART-123', 100.0)
        self.app.customer_entry.insert(0, 'Acme Corp')
        self.app.margin_entry.insert(0, '20')
        self.app.generate_quote('PART-123', 100.0)
        mock_save_quote.assert_called()

    def test_generate_quote_invalid_margin(self):
        self.app.create_quote_screen('PART-123', 100.0)
        self.app.customer_entry.insert(0, 'Acme Corp')
        self.app.margin_entry.insert(0, '-10')
        with self.assertLogs(level='INFO') as cm:
            self.app.generate_quote('PART-123', 100.0)
            self.assertIn('Profit margin cannot be negative', cm.output[0])

if __name__ == '__main__':
    unittest.main()
