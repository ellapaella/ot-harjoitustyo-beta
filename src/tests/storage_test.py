import unittest
import storage

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.store1 = storage.Storage()

    def test_storage_adds_user(self):
        self.store1.add_user("Test")
        self.assertEqual(self.store1.list_length(), 1)