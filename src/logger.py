# logger.py
# Purpose: Provides a utility for automatically logging test results to test_logs.txt.
# Supports test automation for FR1-FR7 by recording test case details.
# Used by gui.py for manual GUI tests and test_*.py for unit tests.
# Ensures logs are stored in the repository root for college submission.

import os
from datetime import datetime

# Get the absolute path to the repository root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, 'test_logs.txt')

def log_test_result(test_case, input_data, output, pass_fail):
    """
    Log a test result to test_logs.txt with timestamp and details.
    
    Parameters:
        test_case (str): Name of the test case (e.g., "FR1: Valid login").
        input_data (str): Input used for the test (e.g., "Username: laurie, Password: moffat123").
        output (str): Observed output (e.g., "Success, navigated to part input").
        pass_fail (str): Test status (e.g., "Pass" or "Fail").
    
    Logic:
        1. Ensures the log file directory exists.
        2. Opens test_logs.txt in append mode using absolute path.
        3. Writes a formatted entry with timestamp, test case, input, output, and pass/fail.
        4. Handles errors by printing them to avoid crashes.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = (
        f"Timestamp: {timestamp}\n"
        f"Test Case: {test_case}\n"
        f"Input: {input_data}\n"
        f"Output: {output}\n"
        f"Pass/Fail: {pass_fail}\n"
        f"{'-'*50}\n"
    )
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except PermissionError:
        print(f"Error: Permission denied writing to {LOG_FILE}")
    except Exception as e:
        print(f"Error logging test result: {e}")
