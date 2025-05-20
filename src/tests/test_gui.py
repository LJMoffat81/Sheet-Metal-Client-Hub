# test_gui.py
# Purpose: Unit tests for the gui module to verify user interface functionality (FR1).
# Tests the login functionality of the SheetMetalClientHub class to ensure correct user authentication.
# Uses unittest and unittest.mock to simulate file operations without modifying data files.
# Logs test results to test_logs.txt using logger.py for college project evaluation.

import unittest
from unittest.mock import patch
from ..gui import SheetMetalClientHub
import tkinter as tk
from ..logger import log_test_result

class TestGUI(unittest.TestCase):
    """
    Test case class for gui.py, focusing on GUI interactions (FR1).
    """
    def setUp(self):
        """
        Set up a Tkinter root window and GUI instance before each test.
        
        Logic:
            1. Creates a Tkinter root window.
            2. Instantiates the SheetMetalClientHub class.
        """
        self.root = tk.Tk()
        self.app = SheetMetalClientHub(self.root)

    def tearDown(self):
        """
        Clean up by destroying the Tkinter root window after each test.
        
        Logic:
            1. Destroys the root window to prevent GUI resource leaks.
        """
        self.root.destroy()

    @patch('file_handler.validate_credentials')
    def test_login_success_user(self, mock_validate):
        """
        Test successful login with valid user credentials (FR1).
        
        Parameters:
            mock_validate: Mock object for validate_credentials function.
        
        Logic:
            1. Mocks validate_credentials to return True.
            2. Enters test username and password.
            3. Calls login method.
            4. Asserts role is "User".
            5. Logs test result to test_logs.txt.
        """
        input_data = "Username: testuser, Password: testpass"
        mock_validate.return_value = True
        try:
            self.app.username_entry.insert(0, "testuser")
            self.app.password_entry.insert(0, "testpass")
            self.app.login()
            self.assertEqual(self.app.role, "User")
            log_test_result(
                test_case="FR1: Valid user login",
                input_data=input_data,
                output="Role set to User",
                pass_fail="Pass"
            )
        except AssertionError as e:
            log_test_result(
                test_case="FR1: Valid user login",
                input_data=input_data,
                output=f"AssertionError: {e}",
                pass_fail="Fail"
            )
            raise

    @patch('file_handler.validate_credentials')
    def test_login_success_admin(self, mock_validate):
        """
        Test successful login with admin credentials (FR1).
        
        Parameters:
            mock_validate: Mock object for validate_credentials function.
        
        Logic:
            1. Mocks validate_credentials to return True.
            2. Enters admin username and password.
            3. Calls login method.
            4. Asserts role is "Admin".
            5. Logs test result to test_logs.txt.
        """
        input_data = "Username: admin, Password: admin123"
        mock_validate.return_value = True
        try:
            self.app.username_entry.insert(0, "admin")
            self.app.password_entry.insert(0, "admin123")
            self.app.login()
            self.assertEqual(self.app.role, "Admin")
            log_test_result(
                test_case="FR1: Valid admin login",
                input_data=input_data,
                output="Role set to Admin",
                pass_fail="Pass"
            )
        except AssertionError as e:
            log_test_result(
                test_case="FR1: Valid admin login",
                input_data=input_data,
                output=f"AssertionError: {e}",
                pass_fail="Fail"
            )
            raise

    def test_login_empty_fields(self):
        """
        Test login with empty username or password fields (FR1).
        
        Logic:
            1. Clears username and password entry fields.
            2. Calls login method.
            3. Asserts role remains None.
            4. Logs test result to test_logs.txt.
        """
        input_data = "Username: , Password: "
        try:
            self.app.username_entry.delete(0, tk.END)
            self.app.password_entry.delete(0, tk.END)
            self.app.login()
            self.assertIsNone(self.app.role)
            log_test_result(
                test_case="FR1: Login with empty fields",
                input_data=input_data,
                output="Role remains None",
                pass_fail="Pass"
            )
        except AssertionError as e:
            log_test_result(
                test_case="FR1: Login with empty fields",
                input_data=input_data,
                output=f"AssertionError: {e}",
                pass_fail="Fail"
            )
            raise

if __name__ == '__main__':
    unittest.main()
