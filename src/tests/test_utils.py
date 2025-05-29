import unittest
from utils import hash_password

class TestUtils(unittest.TestCase):
    def test_hash_password(self):
        result = hash_password("moffat123")
        self.assertEqual(result, "4b5a1911ddfde19a819157e85312b4aae8915e4968cb983e570da2e1098457e0")