import logging
import os

LOG_DIR = r"C:\Users\Laurie\Proton Drive\tartant\My files\GitHub\Sheet-Metal-Client-Hub\data\log"
os.makedirs(LOG_DIR, exist_ok=True)

def log_test_result(test_case, input_data, output, pass_fail):
    """
    Log test results to a dedicated test log file.
    """
    log_file = os.path.join(LOG_DIR, 'test_logs.txt')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info(f"Test Case: {test_case}, Input: {input_data}, Output: {output}, Pass/Fail: {pass_fail}")

def log_message(title, message, level='info'):
    """
    Log a message with a title to the main log file.
    """
    log_file = os.path.join(LOG_DIR, 'main_output.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    formatted_message = f"{title}: {message}"
    if level.lower() == 'info':
        logging.info(formatted_message)
    elif level.lower() == 'error':
        logging.error(formatted_message)
    else:
        logging.debug(formatted_message)