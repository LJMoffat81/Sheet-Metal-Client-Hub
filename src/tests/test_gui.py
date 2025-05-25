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

class TestGUI(unittest.TestCase):
    def setUp(self):
        os.environ['TESTING_MODE'] = '1'
        self.root = tk.Tk()
        self.app = SheetMetalClientHub(self.root)
        self.file_handler = FileHandler()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        LOG_DIR = os.path.join(self.data_dir, 'log')
        os.makedirs(LOG_DIR, exist_ok=True)
        self.log_file = os.path.join(LOG_DIR, 'test_gui.log')
        logger = logging.getLogger('test_gui_unique')
        logger.handlers.clear()
        logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(self.log_file, mode='w')
        self.handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.handlers = [self.handler]
        logging.info("Test setup initialized")
        self.handler.flush()
        time.sleep(1.0)
        rates_path = os.path.join(self.data_dir, 'rates_global.txt')
        logging.debug(f"Writing rates to: {rates_path}")
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

    def tearDown(self):
        self.root.destroy()
        os.environ['TESTING_MODE'] = '0'
        logger = logging.getLogger('test_gui_unique')
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    def _read_log_file(self):
        logging.debug(f"Reading log file: {self.log_file}")
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                content = f.read()
                logging.debug(f"Log content: {content}")
                return content
        logging.debug("Log file not found")
        return ""

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('gui.FileHandler.validate_credentials')
    def test_login_success_user(self, mock_validate, mock_showerror, mock_showinfo):
        logging.debug("Starting test_login_success_user")
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'laurin')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.handler.flush()
        time.sleep(3.0)
        self.assertIsNotNone(self.app.notebook)
        log_content = self._read_log_file()
        self.assertIn("Success: Login successful as User", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('gui.FileHandler.validate_credentials')
    def test_login_success_admin(self, mock_validate, mock_showerror, mock_showinfo):
        logging.debug("Starting test_login_success_admin")
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'admin')
        self.app.password_entry.insert(0, 'admin123')
        self.app.login()
        self.handler.flush()
        time.sleep(3.0)
        self.assertIsNotNone(self.app.rate_key_entry)
        log_content = self._read_log_file()
        self.assertIn("Success: Login successful as Admin", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_login_invalid(self, mock_showerror, mock_showinfo):
        logging.debug("Starting test_login_invalid")
        self.app.username_entry.insert(0, 'wrong')
        self.app.password_entry.insert(0, 'wrong')
        self.app.login()
        self.handler.flush()
        time.sleep(3.0)
        log_content = self._read_log_file()
        self.assertIn("Error: Invalid username or password", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_login_empty_fields(self, mock_showerror, mock_showinfo):
        logging.debug("Starting test_login_empty_fields")
        self.app.login()
        self.handler.flush()
        time.sleep(3.0)
        log_content = self._read_log_file()
        self.assertIn("Error: Username and password cannot be empty", log_content)

    def test_part_input_screen(self):
        logging.debug("Starting test_part_input_screen")
        self.app.create_part_input_screen()
        self.handler.flush()
        time.sleep(3.0)
        self.assertIsNotNone(self.app.notebook)
        self.assertEqual(self.app.notebook.winfo_exists(), 1)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_welding_sub_option_valid(self, mock_showerror, mock_showinfo):
        logging.debug("Starting test_welding_sub_option_valid")
        self.app.create_part_input_screen()
        self.app.notebook.select(1)
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-67890ABCDE')
        self.app.revision_entry.insert(0, 'A')
        self.app.single_material_var.set('Mild Steel')
        self.app.single_quantity_var.set('10')
        self.app.single_thickness_var.set('1.0')
        self.app.single_lay_flat_length_var.set('1000')
        self.app.single_lay_flat_width_var.set('500')
        self.app.work_centre_vars[0].set('Welding')
        self.app.work_centre_quantity_vars[0].set('100')
        self.app.work_centre_sub_option_vars[0].set('MIG')
        self.app.calculate_and_save()
        self.handler.flush()
        time.sleep(3.0)
        log_content = self._read_log_file()
        self.assertIn("Success: Cost calculated", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_coating_sub_option_valid(self, mock_showerror, mock_showinfo):
        logging.debug("Starting test_coating_sub_option_valid")
        self.app.create_part_input_screen()
        self.app.notebook.select(1)
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-67891ABCDE')
        self.app.revision_entry.insert(0, 'A')
        self.app.single_material_var.set('Mild Steel')
        self.app.single_quantity_var.set('5')
        self.app.single_thickness_var.set('1.0')
        self.app.single_lay_flat_length_var.set('1000')
        self.app.single_lay_flat_width_var.set('500')
        self.app.work_centre_vars[0].set('Coating')
        self.app.work_centre_quantity_vars[0].set('1000')
        self.app.work_centre_sub_option_vars[0].set('Painting')
        self.app.calculate_and_save()
        self.handler.flush()
        time.sleep(3.0)
        log_content = self._read_log_file()
        self.assertIn("Success: Cost calculated", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_fastener_selection_valid(self, mock_showerror, mock_showinfo):
        logging.debug("Starting test_fastener_selection_valid")
        self.app.create_part_input_screen()
        self.app.notebook.select(1)
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-67892ABCDE')
        self.app.revision_entry.insert(0, 'A')
        self.app.single_material_var.set('Mild Steel')
        self.app.single_quantity_var.set('20')
        self.app.single_thickness_var.set('1.0')
        self.app.single_lay_flat_length_var.set('1000')
        self.app.single_lay_flat_width_var.set('500')
        self.app.fastener_type_var.set('Bolts')
        self.app.fastener_count_var.set('50')
        self.app.work_centre_vars[0].set('Cutting')
        self.app.work_centre_quantity_vars[0].set('3000')
        self.app.calculate_and_save()
        self.handler.flush()
        time.sleep(3.0)
        log_content = self._read_log_file()
        self.assertIn("Success: Cost calculated", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_single_part_quantity_invalid(self, mock_showerror, mock_showinfo):
        logging.debug("Starting test_single_part_quantity_invalid")
        self.app.create_part_input_screen()
        self.app.notebook.select(1)
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-67893ABCDE')
        self.app.revision_entry.insert(0, 'A')
        self.app.single_quantity_var.set('Other')
        self.app.single_custom_quantity_entry.insert(0, '-10')
        self.app.work_centre_vars[0].set('Cutting')
        self.app.work_centre_quantity_vars[0].set('100')
        self.app.calculate_and_save()
        self.handler.flush()
        time.sleep(3.0)
        log_content = self._read_log_file()
        self.assertIn("Error: Quantity must be a positive integer", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_part_input_invalid_dimensions(self, mock_showerror, mock_showinfo):
        logging.debug("Starting test_part_input_invalid_dimensions")
        self.app.create_part_input_screen()
        self.app.notebook.select(1)
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'PART-12345ABCDE')
        self.app.revision_entry.insert(0, 'A')
        self.app.single_lay_flat_length_var.set('-100')
        self.app.calculate_and_save()
        self.handler.flush()
        time.sleep(3.0)
        log_content = self._read_log_file()
        self.assertIn("Error: Lay-Flat length must be between 50 and 3000 mm", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_part_input_assembly_no_sub_parts(self, mock_showerror, mock_showinfo):
        logging.debug("Starting test_part_input_assembly_no_sub_parts")
        self.app.create_part_input_screen()
        self.app.notebook.select(0)
        self.app.part_id_entry.delete(0, tk.END)
        self.app.part_id_entry.insert(0, 'ASSY-12345ABCDE')
        self.app.revision_entry.insert(0, 'A')
        self.app.assembly_quantity_var.set('10')
        self.app.work_centre_vars[0].set('Assembly')
        self.app.work_centre_quantity_vars[0].set('10')
        self.app.calculate_and_save()
        self.handler.flush()
        time.sleep(3.0)
        log_content = self._read_log_file()
        self.assertIn("Error: At least one sub-part must be selected for an assembly", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('gui.FileHandler.update_rates')
    def test_update_rate_valid(self, mock_update, mock_showerror, mock_showinfo):
        logging.debug("Starting test_update_rate_valid")
        self.app.create_admin_screen()
        self.app.rate_key_entry.insert(0, 'mild_steel_rate')
        self.app.rate_value_entry.insert(0, '0.3')
        self.app.update_rate()
        self.handler.flush()
        time.sleep(3.0)
        mock_update.assert_called_with('mild_steel_rate', 0.3)
        log_content = self._read_log_file()
        self.assertIn("Success: Rate 'mild_steel_rate' updated to 0.3", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_update_rate_invalid(self, mock_showerror, mock_showinfo):
        logging.debug("Starting test_update_rate_invalid")
        self.app.create_admin_screen()
        self.app.rate_key_entry.insert(0, 'mild_steel_rate')
        self.app.rate_value_entry.insert(0, 'invalid')
        self.app.update_rate()
        self.handler.flush()
        time.sleep(3.0)
        log_content = self._read_log_file()
        self.assertIn("Error: Invalid rate value", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('gui.FileHandler.save_quote')
    def test_generate_quote_valid(self, mock_save_quote, mock_showerror, mock_showinfo):
        logging.debug("Starting test_generate_quote_valid")
        self.app.create_quote_screen('PART-123ABCDE', 100.0)
        self.app.customer_entry.insert(0, 'Acme Corp')
        self.app.margin_entry.insert(0, '20')
        self.app.generate_quote('PART-123ABCDE', 100.0)
        self.handler.flush()
        time.sleep(3.0)
        mock_save_quote.assert_called()
        log_content = self._read_log_file()
        self.assertIn("Success: Quote generated and saved to data/quotes.txt", log_content)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_generate_quote_invalid_margin(self, mock_showerror, mock_showinfo):
        logging.debug("Starting test_generate_quote_invalid_margin")
        self.app.create_quote_screen('PART-125ABCDE', 100.0)
        self.app.customer_entry.insert(0, 'Acme Corp')
        self.app.margin_entry.insert(0, '-10')
        self.app.generate_quote('PART-125ABCDE', 100.0)
        self.handler.flush()
        time.sleep(3.0)
        log_content = self._read_log_file()
        self.assertIn("Error: Profit margin cannot be negative", log_content)

if __name__ == '__main__':
    unittest.main()