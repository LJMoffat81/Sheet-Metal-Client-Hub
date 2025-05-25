import unittest
from unittest.mock import patch, mock_open
import sys
import os
import time
import logging

# Add src/ to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from file_handler import FileHandler

class TestFileHandler(unittest.TestCase):
    def setUp(self):
        self.file_handler = FileHandler()
        self.temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
        os.makedirs(self.temp_dir, exist_ok=True)
        LOG_DIR = r"C:\Users\Laurie\Proton Drive\tartant\My files\GitHub\Sheet-Metal-Client-Hub\data\log"
        os.makedirs(LOG_DIR, exist_ok=True)
        self.log_file = os.path.join(LOG_DIR, 'test_file_handler.log')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(self.log_file, mode='w')
        self.handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.handlers = [self.handler]
        logging.info("Test setup initialized")
        self.handler.flush()
        time.sleep(0.5)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        logger = logging.getLogger()
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('builtins.open', new_callable=mock_open, read_data='test content')
    def test_read_file(self, mock_file, mock_showerror, mock_showinfo):
        test_file = os.path.join(self.temp_dir, 'test.txt')
        mock_file.return_value.__enter__.return_value.read.return_value = 'test content'
        content = self.file_handler.read_file(test_file)
        self.assertEqual(content, 'test content')
        mock_file.assert_called_once_with(test_file, 'r')

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_write_file(self, mock_makedirs, mock_file, mock_showerror, mock_showinfo):
        test_file = os.path.join(self.temp_dir, 'output.txt')
        self.file_handler.write_file(test_file, 'test content')
        mock_file.assert_called_once_with(test_file, 'a')
        mock_file().write.assert_called_once_with('test content\n')

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('os.path.exists')
    def test_file_exists(self, mock_exists, mock_showerror, mock_showinfo):
        test_file = os.path.join(self.temp_dir, 'exists.txt')
        mock_exists.return_value = True
        result = self.file_handler.file_exists(test_file)
        self.assertTrue(result)
        mock_exists.assert_called_once_with(test_file)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('file_handler.FileHandler.read_file')
    def test_process_file(self, mock_read, mock_showerror, mock_showinfo):
        test_file = os.path.join(self.temp_dir, 'test.txt')
        mock_read.return_value = 'test content'
        result = self.file_handler.process_file(test_file)
        self.assertEqual(result, 'TEST CONTENT')
        mock_read.assert_called_once_with(test_file)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('file_handler.FileHandler.read_file')
    def test_process_file_empty_filename(self, mock_read, mock_showerror, mock_showinfo):
        mock_read.return_value = ''
        result = self.file_handler.process_file('')
        self.assertEqual(result, '')
        mock_read.assert_called_once_with('')

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('builtins.open', new_callable=mock_open, read_data='{"mild_steel_rate": 0.2}')
    def test_load_rates(self, mock_file, mock_showerror, mock_showinfo):
        rates = self.file_handler.load_rates()
        self.assertEqual(rates, {"mild_steel_rate": 0.2})

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_output(self, mock_file, mock_showerror, mock_showinfo):
        self.file_handler.save_output(
            part_id='PART-123ABCDE',
            revision='1',
            material='mild steel',
            thickness=1.0,
            length=1000,
            width=500,
            quantity=1,
            total_cost=50.0,
            fastener_types_and_counts=[],
            work_centres=[]
        )
        mock_file().write.assert_called()

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_quote(self, mock_file, mock_showerror, mock_showinfo):
        self.file_handler.save_quote(
            part_id='PART-123ABCDE',
            total_cost=50.0,
            customer_name='Acme',
            profit_margin=20.0,
            fastener_types_and_counts=[]
        )
        mock_file().write.assert_called()

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    @patch('builtins.open', new_callable=mock_open, read_data='laurie:moffat123')
    def test_validate_credentials(self, mock_file, mock_showerror, mock_showinfo):
        result = self.file_handler.validate_credentials('laurie', 'moffat123')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()