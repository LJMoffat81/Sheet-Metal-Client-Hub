import unittest
import sys
import os
from unittest.mock import patch
import tkinter as tk

# Add src/ to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from gui import SheetMetalClientHub

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = SheetMetalClientHub(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('gui.validate_credentials')
    def test_login_success(self, mock_validate):
        mock_validate.return_value = True
        self.app.username_entry.insert(0, 'laurie')
        self.app.password_entry.insert(0, 'moffat123')
        self.app.login()
        self.assertEqual(self.app.role, 'User', "Login should set user role")

    def test_part_input_screen(self):
        self.app.create_part_input_screen()
        self.assertIsNotNone(self.app.part_id_entry, "Part ID entry should exist")

if __name__ == '__main__':
    unittest.main()
