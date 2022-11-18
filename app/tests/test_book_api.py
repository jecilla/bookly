import json
from app.models.user import User
from app.models.book import Book
from django.test import TestCase
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile

small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)

image = SimpleUploadedFile(name='test_image.jpg', content=small_gif,
                           content_type='image/gif')

# Create your tests here.


class BookAPITestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            id=1,
            first_name="Test",
            last_name="User",
            email="testuser@test.com",
            password="@bookly124",
            role=1,
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        self.image = json.dumps(str(''))
        Book.objects.create(
            id=1,
            title="Book1",
            book_cover=self.image,
            author="Jovc",
            date_of_pub=timezone.now(),
            number_of_pages=44,
            number_of_books=4
        )
        Book.objects.create(
            id=2,
            title="Book2",
            book_cover=self.image,
            author="Cilla",
            date_of_pub=timezone.now(),
            number_of_pages=48,
            number_of_books=9
        )
        self.user1 = User.objects.get(email='testuser@test.com')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_book_creation(self):
        """
            Testing the creation of a book
        """

        payload = {
            "title": "Book1",
            "book_cover": image,
            "author": "Jovc",
            "date_of_pub": "2022-10-10",
            "number_of_pages": 44,
            "number_of_books": 4
        }
        dev1 = Book.objects.get(id=1)
        dev1.hard_delete()

        response = self.client.post('/api/book/add', payload,
                                    format='multipart')
        self.assertEqual(response.status_code, 201)

    def test_updating_book(self):
        """
            Testing updating the details of a book
        """

        payload = {
            'title': 'New Book Name',
            # "book_cover": self.image,
            "author": "Jovc",
            "date_of_pub": "2022-10-10",
            "number_of_pages": 44,
            "number_of_books": 4
        }
        
        response = self.client.put('/api/book/update/1', payload,
                                   format='multipart')
        self.assertEqual(response.status_code, 200)

    def test_get_book_by_id(self):
        """
            Testing getting a book by id
        """

        response = self.client.get("/api/book/get/1")
        data = json.loads(response.content)
        self.assertEqual(data['title'], "Book1")

    def test_get_all_books(self):
        """
            Testing getting all books
        """
        response = self.client.get("/api/book/all")
        data = json.loads(response.content)
        b1_name = data['results'][0]["title"]
        b2_name = data['results'][1]["title"]
        self.assertEqual(b1_name, "Book1")
        self.assertEqual(b2_name, "Book2")

    def test_deleting_book(self):
        """
            Testing the deletion of a book
        """
        response = self.client.delete('/api/book/delete/1',
                                      format="json")
        self.assertEqual(response.status_code, 204)
