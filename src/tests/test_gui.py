# test_gui.py
# Purpose: Unit tests for the gui module to verify user interface functionality (FR1, FR2, FR6, FR7).
# Tests the login functionality of the SheetMetalClientHub class to ensure correct user authentication.
# Uses unittest and unittest.mock to simulate file operations without modifying data files.
# Designed for college project evaluation, focusing on critical GUI interactions.

import unittest
from unittest.mock import patch
from gui import SheetMetalClientHub
import tkinter as tk

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
    def test_login_success(self, mock_validate):
        """
        Test successful login with valid credentials (FR1).
        
        Parameters:
            mock_validate: Mock object for validate_credentials function.
        
        Logic:
            1. Mocks validate_credentials to return True (simulating valid credentials).
            2. Enters test username and password into GUI entry fields.
            3. Calls the login method.
            4. Asserts that the role is set to "User" after successful login.
        """
        mock_validate.return_value = True
        self.app.username_entry.insert(0, "testuser")
        self.app.password_entry.insert(0, "testpass")
        self.app.login()
        self.assertEqual(self.app.role, "User")

if __name__ == '__main__':
    unittest.main()
