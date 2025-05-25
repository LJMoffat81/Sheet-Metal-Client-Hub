import unittest
import tkinter as tk
from tkinter import messagebox
from unittest.mock import patch
import os
from gui import SheetMetalClientHub
from file_handler import BASE_DIR

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = SheetMetalClientHub(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_login_success(self):
        """Test successful login with valid credentials (FR1)."""
        self.app.username_entry.insert(0, 'laurie')
        self.app.password_entry.insert(0, 'moffat123')
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app.login()
            mock_info.assert_called_with("Success", "Login successful as User")
        self.assertEqual(self.app.role, 'User', "Should log in as User")

    def test_login_invalid(self):
        """Test login with invalid credentials (FR1)."""
        self.app.username_entry.insert(0, 'laurie')
        self.app.password_entry.insert(0, 'wrongpass')
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app.login()
            mock_error.assert_called_with("Error", "Invalid username or password")
        self.assertIsNone(self.app.role, "Role should remain None")

    def test_login_empty_fields(self):
        """Test login with empty fields (FR1)."""
        self.app.username_entry.insert(0, '')
        self.app.password_entry.insert(0, '')
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app.login()
            mock_error.assert_called_with("Error", "Username and password cannot be empty")
        self.assertIsNone(self.app.role, "Role should remain None")

    def test_part_input_screen(self):
        """Test part input screen creation (FR2)."""
        self.app.create_part_input_screen()
        self.assertIsNotNone(self.app.notebook, "Notebook should be created")
        self.assertEqual(self.app.notebook.tab(0, "text"), "Assembly", "Assembly tab should exist")
        self.assertEqual(self.app.notebook.tab(1, "text"), "Single Part", "Single Part tab should exist")

    def test_part_input_invalid_dimensions(self):
        """Test part input with invalid dimensions (FR2)."""
        self.app.username_entry.insert(0, 'laurie')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.app.create_part_input_screen()
        self.app.notebook.select(1)  # Single Part tab
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-67890')
        self.app.revision_entry.insert(0, '1')  # Set valid revision
        self.app.single_material_var.set('mild steel')
        self.app.single_thickness_var.set('1.0')
        self.app.single_lay_flat_length_var.set('4000')  # Invalid: max 3000
        self.app.single_lay_flat_width_var.set('500')
        self.app.work_centre_vars[0].set('Welding')
        self.app.work_centre_quantity_vars[0].set('500')
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app.calculate_and_save()
            mock_error.assert_called_with("Error", "Lay-Flat length must be between 50 and 3000 mm")

    def test_part_input_assembly(self):
        """Test assembly part input (FR2)."""
        self.app.username_entry.insert(0, 'laurie')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.app.create_part_input_screen()
        self.app.notebook.select(0)  # Assembly tab
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'ASSY-98765')
        self.app.revision_entry.insert(0, '1')
        self.app.assembly_quantity_var.set('10')
        self.app.assembly_sub_parts_var.set('PART-12345')
        self.app.add_sub_part(0)
        self.app.work_centre_vars[0].set('Assembly')
        self.app.work_centre_quantity_vars[0].set('5')
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app.calculate_and_save()
            mock_info.assert_called_once()
            self.assertIn("Success", mock_info.call_args[0][0], "Success message should be shown")

    def test_generate_quote_valid(self):
        """Test valid quote generation (FR7)."""
        self.app.create_quote_screen('PART-67890', 50.0)
        self.app.customer_entry.insert(0, 'Acme Corp')
        self.app.margin_entry.insert(0, '20')
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app.generate_quote('PART-67890', 50.0)
            mock_info.assert_called_with("Success", "Quote generated and saved to data/quotes.txt")

    def test_generate_quote_invalid_margin(self):
        """Test quote generation with invalid margin (FR7)."""
        self.app.create_quote_screen('PART-67890', 50.0)
        self.app.customer_entry.insert(0, 'Acme Corp')
        self.app.margin_entry.insert(0, '-10')
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app.generate_quote('PART-67890', 50.0)
            mock_error.assert_called_with("Error", "Profit margin cannot be negative")

    def test_update_rate_valid(self):
        """Test valid rate update (FR6)."""
        self.app.username_entry.insert(0, 'admin')
        self.app.password_entry.insert(0, 'admin123')
        self.app.login()
        self.app.create_admin_screen()
        self.app.rate_key_entry.insert(0, 'mild_steel_rate')
        self.app.rate_value_entry.insert(0, '0.20')
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app.update_rate()
            mock_info.assert_called_with("Success", "Rate 'mild_steel_rate' updated to 0.2 in data/rates_global.txt")

    def test_update_rate_invalid(self):
        """Test invalid rate update (FR6)."""
        self.app.username_entry.insert(0, 'admin')
        self.app.password_entry.insert(0, 'admin123')
        self.app.login()
        self.app.create_admin_screen()
        self.app.rate_key_entry.insert(0, 'mild_steel_rate')
        self.app.rate_value_entry.insert(0, '-0.20')
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app.update_rate()
            mock_error.assert_called_with("Error", "Rate value cannot be negative")

if __name__ == '__main__':
    unittest.main()
