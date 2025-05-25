import unittest
import file_handler

class TestDebugFileHandler(unittest.TestCase):
    def test_file_handler_contents(self):
        print("file_handler.__file__:", file_handler.__file__)
        print("dir(file_handler):", dir(file_handler))
        self.assertTrue(hasattr(file_handler, 'FileHandler'), "FileHandler class not found")
        self.assertTrue(hasattr(file_handler.FileHandler, 'load_rates'), "load_rates not found")
        self.assertTrue(hasattr(file_handler.FileHandler, 'validate_credentials'), "validate_credentials not found")

if __name__ == '__main__':
    unittest.main()
