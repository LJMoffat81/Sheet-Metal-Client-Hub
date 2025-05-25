import unittest
from unittest.mock import patch
import tkinter as tk
from gui import SheetMetalClientHub
from file_handler import FileHandler  # Import the class

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = SheetMetalClientHub(self.root)
        self.file_handler = FileHandler()  # Create an instance

    def tearDown(self):
        self.root.destroy()

    @patch.object(FileHandler, 'validate_credentials')  # Patch the class method
    def test_login_success(self, mock_validate):
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'laurie')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.assertEqual(self.app.role, 'User', "Login should set user role")

if __name__ == '__main__':
    unittest.main()
