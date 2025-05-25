import unittest
from unittest.mock import patch
import tkinter as tk
from gui import SheetMetalClientHub
from file_handler import FileHandler

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = SheetMetalClientHub(self.root)
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
        self.app.rate_key_entry.insert(0, 'mild_steel_rate')
        self.app.rate_value_entry.insert(0, '0.3')
        self.app.update_rate()
        mock_update.assert_called_with('mild_steel_rate', 0.3)

    @patch('gui.FileHandler.validate_credentials')
    @patch('gui.FileHandler.save_output')
    @patch('gui.FileHandler.save_quote')
    def test_full_workflow_user_single_part(self, mock_save_quote, mock_save_output, mock_validate):
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'laurie')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.app.notebook.select(1)  # Single Part tab
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-67890')
        self.app.revision_entry.insert(0, 'A')
        self.app.single_material_var.set('mild_steel')
        self.app.single_thickness_var.set('1.0')
        self.app.single_lay_flat_length_var.set('1000')
        self.app.single_lay_flat_width_var.set('500')
        self.app.work_centre_vars[0].set('Cutting')
        self.app.work_centre_quantity_vars[0].set('3000')
        self.app.work_centre_vars[1].set('Bending')
        self.app.work_centre_quantity_vars[1].set('2')
        self.app.calculate_and_save()
        self.app.create_quote_screen('PART-67890', 50.0)
        self.app.customer_entry.insert(0, 'Acme Corp')
        self.app.margin_entry.insert(0, '20')
        self.app.generate_quote('PART-67890', 50.0)
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
        self.app.notebook.select(0)  # Assembly tab
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'ASSY-98765')
        self.app.revision_entry.insert(0, 'A')
        self.app.assembly_quantity_var.set('10')
        self.app.assembly_sub_parts_var.set('PART-12345')
        self.app.add_sub_part(0)
        self.app.work_centre_vars[0].set('Assembly')
        self.app.work_centre_quantity_vars[0].set('10')
        self.app.calculate_and_save()
        self.app.create_quote_screen('ASSY-98765', 100.0)
        self.app.customer_entry.insert(0, 'Beta Inc')
        self.app.margin_entry.insert(0, '15')
        self.app.generate_quote('ASSY-98765', 100.0)
        mock_save_output.assert_called()
        mock_save_quote.assert_called()

    def test_invalid_login(self):
        self.app.username_entry.insert(0, 'wrong')
        self.app.password_entry.insert(0, 'wrong')
        with self.assertLogs(level='INFO') as cm:
            self.app.login()
            self.assertIn('Invalid credentials', cm.output[0])

    def test_invalid_part_input(self):
        self.app.create_part_input_screen()
        self.app.notebook.select(1)  # Single Part tab
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-123')
        self.app.revision_entry.insert(0, 'A')
        self.app.single_thickness_var.set('-1.0')
        with self.assertLogs(level='INFO') as cm:
            self.app.calculate_and_save()
            self.assertIn('Thickness must be between 1.0 and 3.0 mm', cm.output[0])

    @patch('gui.FileHandler.load_rates')
    def test_empty_rates_file(self, mock_load_rates):
        mock_load_rates.return_value = {}
        self.app.create_part_input_screen()
        self.app.notebook.select(1)  # Single Part tab
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-123')
        self.app.revision_entry.insert(0, 'A')
        self.app.single_material_var.set('mild_steel')
        self.app.single_thickness_var.set('1.0')
        self.app.single_lay_flat_length_var.set('1000')
        self.app.single_lay_flat_width_var.set('500')
        self.app.work_centre_vars[0].set('Cutting')
        self.app.work_centre_quantity_vars[0].set('100')
        with self.assertLogs(level='INFO') as cm:
            self.app.calculate_and_save()
            self.assertIn('Failed to load rates from data/rates_global.txt', cm.output[0])

if __name__ == '__main__':
    unittest.main()
