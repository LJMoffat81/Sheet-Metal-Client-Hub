import logging
import os

# Set up logging to file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_file = os.path.join(BASE_DIR, 'gui.log')

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_test_result(test_case, input_data, output, pass_fail):
    """Log test results to gui.log."""
    logging.info(f"Test Case: {test_case}")
    logging.info(f"Input: {input_data}")
    logging.info(f"Output: {output}")
    logging.info(f"Pass/Fail: {pass_fail}")
    logging.info("-" * 50)
