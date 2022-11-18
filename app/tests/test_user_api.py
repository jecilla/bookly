import json
from app.models.user import User
from django.test import TestCase
from rest_framework.test import APIClient

# Create your tests here.


class UserAPITestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            id=1,
            first_name="New",
            last_name="User",
            email="newuser@test.com",
            password="@matset124",
            role=1,
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        User.objects.create_user(
            id=2,
            first_name="Another",
            last_name="Person",
            email="anotherperson@test.com",
            password="@bookly124",
            role=1
        )
        self.user1 = User.objects.get(email='newuser@test.com')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_user_creation(self):
        """
            Testing the creation of a user
        """

        payload = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@gmail.com',
            'role': 1
        }
        user1 = User.objects.get(id=1)
        user1.hard_delete()

        response = self.client.post('/api/user/adduser', payload,
                                    format='json')
        self.assertEqual(response.status_code, 201)

    def test_updating_user(self):
        """
            Testing updating the details of a user
        """

        payload = {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@gmail.com',
            'role': 1
        }

        response = self.client.put('/api/user/updateuser/1', payload,
                                   format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):

        response = self.client.get("/api/user/getuser/1")
        data = json.loads(response.content)
        self.assertEqual(data['first_name'], "New")

    def test_get_all_users(self):

        response = self.client.get("/api/user/allusers")
        data = json.loads(response.content)
        user1_name = data['results'][0]["first_name"]
        user2_name = data['results'][1]["first_name"]
        self.assertEqual(user1_name, "New")
        self.assertEqual(user2_name, "Another")

    def test_deleting_user(self):
        """
            Testing the deletion of a user
        """
        response = self.client.delete('/api/user/deleteuser/1', format="json")
        self.assertEqual(response.status_code, 204)
