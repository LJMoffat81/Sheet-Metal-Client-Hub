import unittest
import tkinter as tk
from tkinter import messagebox
from unittest.mock import patch
import os
import json
from gui import SheetMetalClientHub
from file_handler import BASE_DIR

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = SheetMetalClientHub(self.root)
        self.output_file = os.path.join(BASE_DIR, 'data/output.txt')
        self.quotes_file = os.path.join(BASE_DIR, 'data/quotes.txt')
        # Clear quotes file to ensure clean state
        with open(self.quotes_file, 'w') as f:
            f.write('')

    def tearDown(self):
        self.root.destroy()

    def test_full_workflow_user(self):
        """Test end-to-end workflow for a user (FR1-FR5, FR7)."""
        # Simulate login (FR1)
        self.app.username_entry.insert(0, 'laurie')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.assertEqual(self.app.role, 'User', "Should log in as User")

        # Navigate to part input screen (FR2)
        self.app.create_part_input_screen()

        # Test single part input (FR2-FR4)
        self.app.notebook.select(1)  # Single Part tab
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-67890')
        self.app.revision_entry.insert(0, '1')
        self.app.single_material_var.set('mild steel')
        self.app.single_thickness_var.set('1.0')
        self.app.single_lay_flat_length_var.set('1000')
        self.app.single_lay_flat_width_var.set('500')
        self.app.work_centre_vars[0].set('Welding')
        self.app.work_centre_quantity_vars[0].set('500.0')
        self.app.single_sub_parts_var.set('FAS-001: Screw M3')
        self.app.add_sub_part(1)

        with patch('tkinter.messagebox.showinfo') as mock_info, patch('tkinter.messagebox.showerror') as mock_error:
            self.app.calculate_and_save()
            mock_info.assert_called_once()
            self.assertIn("Success", mock_info.call_args[0][0], "Success message should be shown")

        # Verify output (FR5)
        with open(self.output_file, 'r') as f:
            lines = f.readlines()
        self.assertTrue(any('PART-67890' in line for line in lines), "Part should be saved to output.txt")

        # Test quote generation (FR7)
        self.app.create_quote_screen('PART-67890', 50.0)
        self.app.customer_entry.insert(0, 'Acme Corp')
        self.app.margin_entry.insert(0, '20')
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app.generate_quote('PART-67890', 50.0)
            mock_info.assert_called_with("Success", "Quote generated and saved to data/quotes.txt")

        # Verify quote
        quotes = []
        try:
            with open(self.quotes_file, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            quotes.append(json.loads(line.strip()))
                        except json.JSONDecodeError:
                            continue
        except FileNotFoundError:
            pass
        self.assertTrue(any(q['part_id'] == 'PART-67890' for q in quotes), "Quote should be saved")

    def test_admin_rate_update(self):
        """Test admin workflow for rate updates (FR1, FR6)."""
        # Simulate admin login (FR1)
        self.app.username_entry.insert(0, 'admin')
        self.app.password_entry.insert(0, 'admin123')
        self.app.login()
        self.assertEqual(self.app.role, 'Admin', "Should log in as Admin")

        # Navigate to admin screen (FR6)
        self.app.create_admin_screen()
        self.app.rate_key_entry.insert(0, 'mild_steel_rate')
        self.app.rate_value_entry.insert(0, '0.20')
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app.update_rate()
            mock_info.assert_called_with("Success", "Rate 'mild_steel_rate' updated to 0.2 in data/rates_global.txt")

        # Verify rate update
        with open(self.rates_file, 'r') as f:
            rates = json.load(f)
        self.assertEqual(rates['mild_steel_rate'], 0.20, "Rate should be updated")

if __name__ == '__main__':
    unittest.main()
