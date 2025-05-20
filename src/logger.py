# logger.py
# Purpose: Handles logging of test results for the Sheet Metal Client Hub.
# Writes test case results to data/test_logs.txt for tracking application behavior.

import os
import datetime

# Get the absolute path to the repository root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def log_test_result(test_case, input_data, output, pass_fail):
    """
    Log test result to data/test_logs.txt.
    
    Parameters:
        test_case (str): Name of the test case.
        input_data (str): Input data used in the test.
        output (str): Output or result of the test.
        pass_fail (str): Pass or Fail status.
    
    Logic:
        1. Formats the log entry with timestamp, test case, input, output, and status.
        2. Appends the entry to data/test_logs.txt.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Test: {test_case}, Input: {input_data}, Output: {output}, Status: {pass_fail}\n"
    try:
        with open(os.path.join(BASE_DIR, 'data/test_logs.txt'), 'a') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to log file: {e}")
