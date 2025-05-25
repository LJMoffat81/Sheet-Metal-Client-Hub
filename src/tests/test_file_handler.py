import unittest
import os
import logging
import json
import sys

# Add src/ to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from file_handler import FileHandler

class TestFileHandler(unittest.TestCase):
    def setUp(self):
        self.file_handler = FileHandler()
        LOG_DIR = r"C:\Users\Laurie\Proton Drive\tartant\My files\GitHub\Sheet-Metal-Client-Hub\data\log"
        os.makedirs(LOG_DIR, exist_ok=True)
        self.log_file = os.path.join(LOG_DIR, 'file_handler.log')
        logger = logging.getLogger('test_file_handler')
        logger.handlers.clear()
        logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(self.log_file, mode='a')
        self.handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.handlers = [self.handler]
        logging.info("Test setup initialized")
        self.handler.flush()

        # Setup test files
        self.test_dir = os.path.join(os.path.dirname(__file__), 'temp')
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_file = os.path.join(self.test_dir, 'test.txt')
        self.rates_file = os.path.join(self.test_dir, 'rates.txt')
        self.output_file = os.path.join(self.test_dir, 'output.txt')
        self.quotes_file = os.path.join(self.test_dir, 'quotes.txt')

    def tearDown(self):
        logger = logging.getLogger('test_file_handler')
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    def test_file_exists(self):
        with open(self.test_file, 'w') as f:
            f.write('test content')
        self.assertTrue(self.file_handler.file_exists(self.test_file))

    def test_read_file(self):
        content = 'test content'
        with open(self.test_file, 'w') as f:
            f.write(content)
        result = self.file_handler.read_file(self.test_file)
        self.assertEqual(result, content)

    def test_write_file(self):
        content = 'test content'
        self.file_handler.write_file(self.test_file, content)
        with open(self.test_file, 'r') as f:
            result = f.read()
        self.assertEqual(result, content)

    def test_process_file(self):
        content = 'line1\nline2\nline3'
        with open(self.test_file, 'w') as f:
            f.write(content)
        result = self.file_handler.process_file(self.test_file)
        self.assertEqual(result, ['line1', 'line2', 'line3'])

    def test_process_file_empty_filename(self):
        with self.assertRaises(ValueError):
            self.file_handler.process_file('')

    def test_load_rates(self):
        rates = {
            'mild_steel_rate': 0.0001,
            'cutting_rate_per_mm': 0.01
        }
        with open(self.rates_file, 'w') as f:
            json.dump(rates, f)
        result = self.file_handler.load_rates(self.rates_file)
        self.assertEqual(result, rates)

    def test_save_output(self):
        part_id = 'PART-123'
        revision = 'A'
        material = 'Mild Steel'
        thickness = 1.0
        length = 1000
        width = 500
        quantity = 10
        total_cost = 100.0
        fastener_types_and_counts = [('Bolts', 50)]
        work_centres = [('Cutting', 1000, 'None')]
        self.file_handler.save_output(part_id, revision, material, thickness, length, width, quantity, total_cost, fastener_types_and_counts, work_centres)
        with open('data/output.txt', 'r') as f:
            content = f.read()
        expected = f"{part_id},{revision},{material},{thickness},{length},{width},{quantity},{total_cost},{fastener_types_and_counts},{work_centres}\n"
        self.assertIn(expected, content)

    def test_save_quote(self):
        part_id = 'PART-123'
        total_cost = 100.0
        customer_name = 'Acme Corp'
        profit_margin = 20.0
        fastener_types_and_counts = [('Bolts', 50)]
        self.file_handler.save_quote(part_id, total_cost, customer_name, profit_margin, fastener_types_and_counts)
        with open('data/quotes.txt', 'r') as f:
            content = f.read()
        expected = f"{part_id},{total_cost},{customer_name},{profit_margin},{fastener_types_and_counts}\n"
        self.assertIn(expected, content)

    def test_validate_credentials(self):
        self.assertTrue(self.file_handler.validate_credentials('laurie', 'moffat123'))
        self.assertFalse(self.file_handler.validate_credentials('wrong', 'wrong'))

if __name__ == '__main__':
    unittest.main()