import unittest
from unittest.mock import patch
import tkinter as tk
import sys
import os
import time
import logging

# Add src/ to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gui import SheetMetalClientHub
from file_handler import FileHandler

class TestSystem(unittest.TestCase):
    def setUp(self):
        os.environ['TESTING_MODE'] = '1'
        self.root = tk.Tk()
        self.app = SheetMetalClientHub(self.root)
        self.file_handler = FileHandler()
        LOG_DIR = r"C:\Users\Laurie\Proton Drive\tartant\My files\GitHub\Sheet-Metal-Client-Hub\data\log"
        os.makedirs(LOG_DIR, exist_ok=True)
        self.log_file = os.path.join(LOG_DIR, 'test_system.log')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(self.log_file, mode='w')
        self.handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.handlers = [self.handler]
        logging.info("Test setup initialized")
        self.handler.flush()
        time.sleep(0.5)
        rates_path = os.path.join(os.path.dirname(__file__), '../../data/rates_global.txt')
        with open(rates_path, 'w') as f:
            f.write('''
            {
                "mild_steel_rate": 0.0001,
                "aluminium_rate": 0.00015,
                "stainless_steel_rate": 0.0002,
                "cutting_rate_per_mm": 0.01,
                "bending_rate_per_bend": 0.5,
                "mig_welding_rate_per_mm": 0.02,
                "tig_welding_rate_per_mm": 0.025,
                "painting_rate_per_mm²": 0.001,
                "coating_rate_per_mm²": 0.0015,
                "assembly_rate_per_component": 0.8,
                "finishing_rate_per_mm²": 0.002,
                "drilling_rate_per_hole": 0.1,
                "punching_rate_per_punch": 0.15,
                "grinding_rate_per_mm²": 0.003,
                "inspection_rate_per_unit": 0.2,
                "bolts_rate_per_unit": 0.1,
                "rivets_rate_per_unit": 0.08,
                "screws_rate_per_unit": 0.09
            }
            ''')
        output_path = os.path.join(os.path.dirname(__file__), '../../data/output.txt')
        with open(output_path, 'w') as f:
            f.write('PART-12345ABCDE,A,Mild Steel,1.0,1000,500,1,50.0,[],[]\n')

    def tearDown(self):
        self.root.destroy()
        os.environ['TESTING_MODE'] = '0'
        logger = logging.getLogger()
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    def _read_log_file(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                return f.read()
        return ""

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('gui.FileHandler.validate_credentials')
    @patch('gui.FileHandler.update_rates')
    def test_admin_rate_update(self, mock_update, mock_validate, mock_showerror, mock_showinfo):
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'admin')
        self.app.password_entry.insert(0, 'admin123')
        self.app.login()
        self.app.rate_key_entry.insert(0, 'mild_steel_rate')
        self.app.rate_value_entry.insert(0, '0.3')
        self.app.update_rate()
        mock_update.assert_called_with('mild_steel_rate', 0.3)
        log_content = self._read_log_file()
        self.assertIn("Success: Rate 'mild_steel_rate' updated to 0.3", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('gui.FileHandler.validate_credentials')
    @patch('gui.FileHandler.save_output')
    @patch('gui.FileHandler.save_quote')
    def test_full_workflow_user_single_part_with_welding(self, mock_save_quote, mock_save_output, mock_validate, mock_showerror, mock_showinfo):
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'laurin')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.app.notebook.select(1)
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-67890ABCDE')
        self.app.revision_entry.insert(0, 'A')
        self.app.single_material_var.set('Mild Steel')
        self.app.single_thickness_var.set('1.0')
        self.app.single_lay_flat_length_var.set('1000')
        self.app.single_lay_flat_width_var.set('500')
        self.app.single_quantity_var.set('10')
        self.app.work_centre_vars[0].set('Welding')
        self.app.work_centre_quantity_vars[0].set('100')
        self.app.work_centre_sub_option_vars[0].set('MIG')
        self.app.calculate_and_save()
        self.app.create_quote_screen('PART-67890ABCDE', 50.0)
        self.app.customer_entry.insert(0, 'Acme Corp')
        self.app.margin_entry.insert(0, '20')
        self.app.generate_quote('PART-67890ABCDE', 50.0)
        mock_save_output.assert_called()
        mock_save_quote.assert_called()
        log_content = self._read_log_file()
        self.assertIn("Success: Quote generated and saved to data/quotes.txt", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('gui.FileHandler.validate_credentials')
    @patch('gui.FileHandler.save_output')
    @patch('gui.FileHandler.save_quote')
    def test_full_workflow_user_single_part_with_fasteners(self, mock_save_quote, mock_save_output, mock_validate, mock_showerror, mock_showinfo):
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'laurin')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.app.notebook.select(1)
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-67891ABCDE')
        self.app.revision_entry.insert(0, 'A')
        self.app.single_material_var.set('Mild Steel')
        self.app.single_thickness_var.set('1.0')
        self.app.single_lay_flat_length_var.set('1000')
        self.app.single_lay_flat_width_var.set('500')
        self.app.single_quantity_var.set('5')
        self.app.fastener_type_var.set('Bolts')
        self.app.fastener_count_var.set('50')
        self.app.work_centre_vars[0].set('Cutting')
        self.app.work_centre_quantity_vars[0].set('3000')
        self.app.calculate_and_save()
        self.app.create_quote_screen('PART-67891ABCDE', 50.0)
        self.app.customer_entry.insert(0, 'Acme Corp')
        self.app.margin_entry.insert(0, '20')
        self.app.generate_quote('PART-67891ABCDE', 50.0)
        mock_save_output.assert_called()
        mock_save_quote.assert_called()
        log_content = self._read_log_file()
        self.assertIn("Success: Quote generated and saved to data/quotes.txt", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('gui.FileHandler.validate_credentials')
    @patch('gui.FileHandler.save_output')
    @patch('gui.FileHandler.save_quote')
    def test_assembly_workflow(self, mock_save_quote, mock_save_output, mock_validate, mock_showerror, mock_showinfo):
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'laurin')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.app.notebook.select(0)
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'ASSY-98765ABCDE')
        self.app.revision_entry.insert(0, 'A')
        self.app.assembly_quantity_var.set('10')
        self.app.assembly_sub_parts_var.set('PART-12345ABCDE')
        self.app.add_sub_part(0)
        self.app.work_centre_vars[0].set('Assembly')
        self.app.work_centre_quantity_vars[0].set('10')
        self.app.calculate_and_save()
        self.app.create_quote_screen('ASSY-98765ABCDE', 100.0)
        self.app.customer_entry.insert(0, 'Beta Inc')
        self.app.margin_entry.insert(0, '15')
        self.app.generate_quote('ASSY-98765ABCDE', 100.0)
        mock_save_output.assert_called()
        mock_save_quote.assert_called()
        log_content = self._read_log_file()
        self.assertIn("Success: Quote generated and saved to data/quotes.txt", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_invalid_login(self, mock_showerror, mock_showinfo):
        self.app.username_entry.insert(0, 'wrong')
        self.app.password_entry.insert(0, 'wrong')
        self.app.login()
        log_content = self._read_log_file()
        self.assertIn("Error: Invalid username or password", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_invalid_part_input(self, mock_showerror, mock_showinfo):
        self.app.create_part_input_screen()
        self.app.notebook.select(1)
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-123ABCDE')
        self.app.revision_entry.insert(0, 'A')
        self.app.single_thickness_var.set('-1.0')
        self.app.calculate_and_save()
        log_content = self._read_log_file()
        self.assertIn("Error: Thickness must be between 1.0 and 3.0 mm", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('gui.FileHandler.load_rates')
    def test_empty_rates_file(self, mock_load_rates, mock_showerror, mock_showinfo):
        mock_load_rates.return_value = {}
        self.app.create_part_input_screen()
        self.app.notebook.select(1)
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-123ABCDE')
        self.app.revision_entry.insert(0, 'A')
        self.app.single_material_var.set('Mild Steel')
        self.app.single_thickness_var.set('1.0')
        self.app.single_lay_flat_length_var.set('1000')
        self.app.single_lay_flat_width_var.set('500')
        self.app.work_centre_vars[0].set('Cutting')
        self.app.work_centre_quantity_vars[0].set('100')
        self.app.calculate_and_save()
        log_content = self._read_log_file()
        self.assertIn("Error: Failed to load rates from data/rates_global.txt", log_content)

if __name__ == '__main__':
    unittest.main()