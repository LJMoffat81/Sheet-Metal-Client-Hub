import os
import unittest
from unittest.mock import patch
import tempfile

class TestFileUtils(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('os.path.join')
    def test_create_directory(self, mock_join):
        mock_join.side_effect = lambda *args: f"{self.temp_dir}/{args[-1]}" if args else self.temp_dir
        dir_name = "new_dir"
        full_path = f"{self.temp_dir}/{dir_name}"
        os.makedirs(full_path, exist_ok=True)
        self.assertTrue(os.path.exists(full_path))

    @patch('os.path.join')
    def test_get_file_extension(self, mock_join):
        mock_join.side_effect = lambda *args: f"{self.temp_dir}/{args[-1]}" if args else self.temp_dir
        filename = "document.pdf"
        full_path = f"{self.temp_dir}/{filename}"
        extension = os.path.splitext(full_path)[1]
        self.assertEqual(extension, ".pdf")

if __name__ == '__main__':
    unittest.main()
