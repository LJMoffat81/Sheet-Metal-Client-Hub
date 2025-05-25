import logging
import os

# Set up logging to file
LOG_DIR = r"C:\Users\Laurie\Proton Drive\tartant\My files\GitHub\Sheet-Metal-Client-Hub\data\log"
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, 'gui.log')

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

def log_message(level, message):
    """Log a message to gui.log."""
    if level == 'info':
        logging.info(message)
    elif level == 'error':
        logging.error(message)