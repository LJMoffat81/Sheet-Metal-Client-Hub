import os
import unittest
from unittest.mock import patch, mock_open
import tempfile
from file_handler import FileHandler

class TestFileHandler(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.file_handler = FileHandler()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('os.path.join')
    def test_process_file(self, mock_join):
        mock_join.side_effect = lambda *args: f"{self.temp_dir}/{args[-1]}" if args else self.temp_dir
        test_file = "test.txt"
        result = self.file_handler.process_file(test_file)
        expected = f"{self.temp_dir}/{test_file}"
        self.assertEqual(result, expected)

    @patch('os.path.join')
    @patch('builtins.open', new_callable=mock_open, read_data="test content")
    def test_read_file(self, mock_file, mock_join):
        mock_join.side_effect = lambda *args: f"{self.temp_dir}/{args[-1]}" if args else self.temp_dir
        test_file = "test.txt"
        content = self.file_handler.read_file(test_file)
        self.assertEqual(content, "test content")
        mock_file.assert_called_once_with(f"{self.temp_dir}/{test_file}", 'r')

    @patch('os.path.join')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_file(self, mock_file, mock_join):
        mock_join.side_effect = lambda *args: f"{self.temp_dir}/{args[-1]}" if args else self.temp_dir
        test_file = "output.txt"
        content = "new content"
        self.file_handler.write_file(test_file, content)
        mock_file.assert_called_once_with(f"{self.temp_dir}/{test_file}", 'w')
        mock_file().write.assert_called_once_with(content)

    @patch('os.path.join')
    @patch('os.path.exists')
    def test_file_exists(self, mock_exists, mock_join):
        mock_join.side_effect = lambda *args: f"{self.temp_dir}/{args[-1]}" if args else self.temp_dir
        mock_exists.return_value = True
        test_file = "exists.txt"
        result = self.file_handler.file_exists(test_file)
        self.assertTrue(result)
        mock_exists.assert_called_once_with(f"{self.temp_dir}/{test_file}")

    @patch('os.path.join')
    @patch('os.path.exists')
    def test_file_does_not_exist(self, mock_exists, mock_join):
        mock_join.side_effect = lambda *args: f"{self.temp_dir}/{args[-1]}" if args else self.temp_dir
        mock_exists.return_value = False
        test_file = "missing.txt"
        result = self.file_handler.file_exists(test_file)
        self.assertFalse(result)
        mock_exists.assert_called_once_with(f"{self.temp_dir}/{test_file}")

    @patch('os.path.join')
    @patch('builtins.open', new_callable=mock_open)
    def test_process_file_empty_filename(self, mock_file, mock_join):
        mock_join.side_effect = lambda *args: f"{self.temp_dir}/{args[-1]}" if args else self.temp_dir
        test_file = ""
        result = self.file_handler.process_file(test_file)
        expected = f"{self.temp_dir}/"
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
