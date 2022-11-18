from django.test import TestCase
from app.models.user import User
from django.core.exceptions import ValidationError

# Create your tests here.

class UserTestCase(TestCase):
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


    def test_user_created(self):
        user1 = User.objects.get(email = 'newuser@test.com')
        user2 = User.objects.get(first_name = 'Another')
        self.assertEqual(user1.last_name, 'User')
        self.assertEqual(user2.email, 'anotherperson@test.com')

    def test_create_user_with_invalid_email(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                first_name = 'Invalid',
                last_name = 'Email',
                email = 'newuser@test,com',
                password = '@bookly124'
            )

