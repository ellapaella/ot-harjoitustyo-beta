
import unittest
import user


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = user.User("test_user", "test_password")

    def test_user_is_created(self):
        self.assertNotEqual(self.user, None)

    def test_user_has_right_name(self):
        self.assertEqual(self.user.name, "test_user")
