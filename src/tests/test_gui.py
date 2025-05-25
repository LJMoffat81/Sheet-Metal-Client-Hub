import unittest
import sys
import os
from unittest.mock import patch
import tkinter as tk
from tkinter import messagebox
from file_handler import FileHandler
from gui import SheetMetalClientHub

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = SheetMetalClientHub(self.root)
        self.file_handler = FileHandler()

    def tearDown(self):
        self.root.destroy()

    @patch.object(FileHandler, 'validate_credentials')
    def test_login_success(self, mock_validate):
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'laurie')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.assertEqual(self.app.role, 'User', "Login should set user role")

    @patch.object(FileHandler, 'validate_credentials')
    @patch('tkinter.messagebox.showerror')
    def test_login_invalid(self, mock_showerror, mock_validate):
        mock_validate.return_value = False
        self.app.username_entry.insert(0, 'laurie')
        self.app.password_entry.insert(0, 'wrong')
        self.app.login()
        mock_showerror.assert_called_with("Error", "Invalid username or password")
        self.assertIsNone(self.app.role, "Role should remain None on invalid login")

    @patch('tkinter.messagebox.showerror')
    def test_login_empty_fields(self, mock_showerror):
        self.app.username_entry.insert(0, '')
        self.app.password_entry.insert(0, '')
        self.app.login()
        mock_showerror.assert_called_with("Error", "Username and password cannot be empty")
        self.assertIsNone(self.app.role, "Role should remain None on empty fields")

    def test_part_input_screen(self):
        self.app.create_part_input_screen()
        self.assertIsNotNone(self.app.part_id_entry, "Part ID entry should exist")

    def test_part_input_assembly(self):
        self.app.create_part_input_screen()
        self.app.notebook.select(0)  # Assembly tab
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'ASSY-67890')
        self.app.assembly_quantity_var.set('10')
        self.app.assembly_sub_parts_var.set('PART-12345')
        self.app.add_sub_part(0)
        self.assertIn('PART-12345', self.app.assembly_selected_sub_parts, "Sub-part should be added")

    @patch('tkinter.messagebox.showerror')
    def test_part_input_invalid_dimensions(self, mock_showerror):
        self.app.create_part_input_screen()
        self.app.notebook.select(1)  # Single Part tab
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-12345')
        self.app.single_material_var.set('mild steel')
        self.app.single_thickness_var.set('1.0')
        self.app.single_lay_flat_length_var.set('4000')  # Invalid: max 3000
        self.app.single_lay_flat_width_var.set('500')
        self.app.work_centre_vars[0].set('Welding')
        self.app.work_centre_quantity_vars[0].set('500.0')
        self.app.calculate_and_save()
        mock_showerror.assert_called_with("Error", "Lay-Flat length must be between 50 and 3000 mm")

    @patch.object(FileHandler, 'update_rates')
    def test_update_rate_valid(self, mock_update_rates):
        self.app.create_admin_screen()
        self.app.rate_key_entry.insert(0, 'mild_steel_rate')
        self.app.rate_value_entry.insert(0, '0.15')
        self.app.update_rate()
        mock_update_rates.assert_called_with('mild_steel_rate', 0.15)

    @patch('tkinter.messagebox.showerror')
    def test_update_rate_invalid(self, mock_showerror):
        self.app.create_admin_screen()
        self.app.rate_key_entry.insert(0, 'mild_steel_rate')
        self.app.rate_value_entry.insert(0, '-0.1')
        self.app.update_rate()
        mock_showerror.assert_called_with("Error", "Rate value cannot be negative")

    @patch.object(FileHandler, 'save_quote')
    def test_generate_quote_valid(self, mock_save_quote):
        self.app.create_quote_screen('PART-12345', 50.0)
        self.app.customer_entry.insert(0, 'Acme')
        self.app.margin_entry.insert(0, '20')
        self.app.generate_quote('PART-12345', 50.0)
        mock_save_quote.assert_called_with('PART-12345', 50.0, 'Acme', 20.0)

    @patch('tkinter.messagebox.showerror')
    def test_generate_quote_invalid_margin(self, mock_showerror):
        self.app.create_quote_screen('PART-12345', 50.0)
        self.app.customer_entry.insert(0, 'Acme')
        self.app.margin_entry.insert(0, '-10')
        self.app.generate_quote('PART-12345', 50.0)
        mock_showerror.assert_called_with("Error", "Profit margin cannot be negative")

if __name__ == '__main__':
    unittest.main()
