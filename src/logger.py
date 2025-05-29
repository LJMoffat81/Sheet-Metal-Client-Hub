import logging
from logging_config import setup_logger

# Set up logging
logger = setup_logger('logger', 'logger.log')

def log_message(title, message, level='info'):
    """
    Log a message with the specified title and level.
    """
    logger.log(logging.INFO if level == 'info' else logging.ERROR, f"{title}: {message}")
    logger.debug(f"Logged message: {title} - {message} (level={level})")

def log_test_result(test_case, input_data, output, pass_fail):
    """
    Log the result of a test case.
    """
    logger.info(f"Test Case: {test_case}, Input: {input_data}, Output: {output}, Result: {pass_fail}")
    logger.debug(f"Test result logged: {test_case} - {pass_fail}")