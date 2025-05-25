import unittest
import tkinter as tk
from gui import SheetMetalClientHub

class TestDebugGUI(unittest.TestCase):
    def test_gui_initialization(self):
        try:
            root = tk.Tk()
            app = SheetMetalClientHub(root)
            self.assertIsNotNone(app.root, "GUI root window should be initialized")
            self.assertIsNotNone(app.username_entry, "Username entry should exist")
            self.assertIsNotNone(app.password_entry, "Password entry should exist")
            print("GUI initialized successfully")
            root.destroy()
        except Exception as e:
            self.fail(f"GUI initialization failed: {e}")

if __name__ == '__main__':
    unittest.main()
