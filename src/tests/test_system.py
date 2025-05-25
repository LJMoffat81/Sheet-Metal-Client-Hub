import unittest
from unittest.mock import patch
import tkinter as tk
from gui import SheetMetalGUI
from file_handler import FileHandler

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = SheetMetalGUI(self.root)
        self.file_handler = FileHandler()

    def tearDown(self):
        self.root.destroy()

    @patch('gui.FileHandler.validate_credentials')
    @patch('gui.FileHandler.update_rates')
    def test_admin_rate_update(self, mock_update, mock_validate):
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'admin')
        self.app.password_entry.insert(0, 'admin123')
        self.app.login()
        self.app.show_rate_update_screen()
        self.app.rate_key_var.set('mild_steel_rate')
        self.app.rate_value_entry.insert(0, '0.3')
        self.app.update_rate()
        mock_update.assert_called_with('mild_steel_rate', '0.3')

    @patch('gui.FileHandler.validate_credentials')
    @patch('gui.FileHandler.save_output')
    @patch('gui.FileHandler.save_quote')
    def test_full_workflow_user(self, mock_save_quote, mock_save_output, mock_validate):
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'laurie')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.app.show_part_input_screen()
        self.app.part_id_entry.insert(0, 'PART-67890')
        self.app.material_var.set('mild_steel')
        self.app.thickness_entry.insert(0, '1.0')
        self.app.length_entry.insert(0, '1000')
        self.app.width_entry.insert(0, '500')
        self.app.quantity_entry.insert(0, '1')
        self.app.work_centre_var.set(['cutting', 'bending'])
        self.app.submit_part()
        self.app.show_quote_screen()
        self.app.customer_entry.insert(0, 'Acme Corp')
        self.app.margin_entry.insert(0, '20')
        self.app.generate_quote()
        mock_save_output.assert_called()
        mock_save_quote.assert_called()

    @patch('gui.FileHandler.validate_credentials')
    @patch('gui.FileHandler.save_output')
    @patch('gui.FileHandler.save_quote')
    def test_assembly_workflow(self, mock_save_quote, mock_save_output, mock_validate):
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'laurie')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.app.show_part_input_screen()
        self.app.part_id_entry.insert(0, 'ASSY-98765')
        self.app.part_type_var.set('Assembly')
        self.app.quantity_entry.insert(0, '10')
        self.app.submit_part()
        self.app.show_quote_screen()
        self.app.customer_entry.insert(0, 'Beta Inc')
        self.app.margin_entry.insert(0, '15')
        self.app.generate_quote()
        mock_save_output.assert_called()
        mock_save_quote.assert_called()

    def test_invalid_login(self):
        self.app.username_entry.insert(0, 'wrong')
        self.app.password_entry.insert(0, 'wrong')
        with self.assertLogs(level='WARNING') as cm:
            self.app.login()
            self.assertIn('Invalid credentials', cm.output[0])

    def test_invalid_part_input(self):
        self.app.show_part_input_screen()
        self.app.part_id_entry.insert(0, 'PART-123')
        self.app.material_var.set('mild_steel')
        self.app.thickness_entry.insert(0, '-1.0')
        with self.assertLogs(level='ERROR') as cm:
            self.app.submit_part()
            self.assertIn('Invalid dimensions', cm.output[0])

    @patch('gui.FileHandler.load_rates')
    def test_empty_rates_file(self, mock_load_rates):
        mock_load_rates.return_value = {}
        self.app.show_part_input_screen()
        self.app.part_id_entry.insert(0, 'PART-123')
        self.app.material_var.set('mild_steel')
        self.app.thickness_entry.insert(0, '1.0')
        self.app.length_entry.insert(0, '1000')
        self.app.width_entry.insert(0, '500')
        self.app.quantity_entry.insert(0, '1')
        self.app.work_centre_var.set(['cutting'])
        with self.assertLogs(level='ERROR') as cm:
            self.app.submit_part()
            self.assertIn('Missing rate', cm.output[0])

if __name__ == '__main__':
    unittest.main()
