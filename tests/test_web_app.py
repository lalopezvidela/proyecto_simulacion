import os
import tempfile
import unittest

from web_app import create_app


class WebAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "usuarios.db")
        self.app = create_app(db_path=self.db_path)
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_register_and_login_flow(self):
        register_response = self.client.post(
            "/register",
            data={
                "full_name": "Ana Pérez",
                "username": "ana",
                "email": "ana@example.com",
                "password": "clave123",
                "confirm_password": "clave123",
            },
            follow_redirects=True,
        )
        self.assertIn(b"Cuenta creada", register_response.data)

        login_response = self.client.post(
            "/login",
            data={"username": "ana", "password": "clave123"},
            follow_redirects=True,
        )
        self.assertIn(b"Panel principal", login_response.data)


if __name__ == "__main__":
    unittest.main()
