import os
import tempfile
import unittest

from database import authenticate_user, create_tables, register_user


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "usuarios.db")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_register_and_authenticate_user(self):
        create_tables(self.db_path)

        registered = register_user(
            full_name="Ana Pérez",
            username="ana",
            email="ana@example.com",
            password="clave123",
            db_path=self.db_path,
        )

        self.assertTrue(registered)
        self.assertTrue(authenticate_user("ana", "clave123", db_path=self.db_path))
        self.assertFalse(authenticate_user("ana", "clave incorrecta", db_path=self.db_path))

    def test_duplicate_username_is_rejected(self):
        create_tables(self.db_path)

        first = register_user(
            full_name="Luis Gómez",
            username="luis",
            email="luis@example.com",
            password="123456",
            db_path=self.db_path,
        )
        second = register_user(
            full_name="Luis Gómez 2",
            username="luis",
            email="otro@example.com",
            password="654321",
            db_path=self.db_path,
        )

        self.assertTrue(first)
        self.assertFalse(second)


if __name__ == "__main__":
    unittest.main()
