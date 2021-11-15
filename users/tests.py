from rest_framework.test import APITestCase


class UsersTestCase(APITestCase):
    def test_authentication(self):
        user_data = {"username": "test", "password": "test"}
        response = self.client.post("/api/sign-up", user_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.data)

        response = self.client.post("/api/login", user_data, format="json")
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        response = self.client.post("/api/login", user_data, format="json")
