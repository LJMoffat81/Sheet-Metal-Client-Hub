import unittest
from unittest.mock import patch
import tkinter as tk
from gui import SheetMetalClientHub

class TestGUI(unittest.TestCase):
    @patch('file_handler.FileHandler')
    def test_login(self, mock_file_handler):
        mock_file_handler.return_value.validate_credentials.return_value = True
        mock_file_handler.return_value.get_user_role.return_value = "User"
        root = tk.Tk()
        app = SheetMetalClientHub(root)
        app.username_entry.insert(0, "laurie")
        app.password_entry.insert(0, "moffat123")
        result = app.login()
        self.assertEqual(result, "Login successful as User")
        root.destroy()