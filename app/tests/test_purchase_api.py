import json
from app.models.purchase import PurchaseBook
from app.models.user import User
from app.models.book import Book
from django.test import TestCase
from rest_framework.test import APIClient
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)

image = SimpleUploadedFile(name='test_image.jpg', content=small_gif,
                           content_type='image/gif')

# Create your tests here.


class PurchaseBookAPITestCase(TestCase):
    def setUp(self):
        u1=User.objects.create_user(
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
        u2=User.objects.create_user(
            id=2,
            first_name="Another",
            last_name="Person",
            email="anotherperson@test.com",
            password="@bookly124",
            role=1
        )
        self.image = json.dumps(str(''))
        b1=Book.objects.create(
            id=1,
            title="Book1",
            book_cover=self.image,
            author="Jovc",
            date_of_pub=timezone.now(),
            number_of_pages=44,
            number_of_books=4
        )
        b2=Book.objects.create(
            id=2,
            title="Book2",
            book_cover=self.image,
            author="Lori",
            date_of_pub=timezone.now(),
            number_of_pages=44,
            number_of_books=4
        )
        p1 = PurchaseBook.objects.create(
            id=1,
            book=b1,
            purchased_by=u1,
            date_purchased=timezone.now()
        )
        p2 = PurchaseBook.objects.create(
            id=2,
            book=b2,
            purchased_by=u2,
            date_purchased=timezone.now()
        )
        self.user1 = User.objects.get(email='testuser@test.com')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_purchase_book_creation(self):
        """
            Testing the creation of a purchase book
        """

        payload = {
            "book": 1,
            "purchased_by": 1,
            "date_purchased": timezone.now()
        }
        p1 = PurchaseBook.objects.get(id=1)
        p1.hard_delete()

        response = self.client.post('/api/purchase/add', payload,
                                    format='json')
        self.assertEqual(response.status_code, 201)

    def test_updating_purchase_book(self):
        """
            Testing updating the details of a purchase book
        """

        payload = {
            "book": 1,
            "purchased_by": 1,
            "date_purchased": timezone.now()
        }

        response = self.client.put('/api/purchase/update/1', payload,
                                   format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_purchase_book_by_id(self):
        """
            Testing getting a purchase book by id
        """

        response = self.client.get("/api/purchase/get/1")
        data = json.loads(response.content)
        self.assertEqual(data['purchased_by'], 1)

    def test_get_all_purchase_books(self):
        """
            Testing getting all purchase books
        """
        response = self.client.get("/api/purchase/all")
        data = json.loads(response.content)
        p1 = data['results'][0]["purchased_by"]
        p2 = data['results'][1]["book"]
        self.assertEqual(p1, 1)
        self.assertEqual(p2, 2)

    def test_deleting_purchase_book(self):
        """
            Testing the deletion of a purchase_book
        """
        response = self.client.delete('/api/purchase/delete/1',
                                      format="json")
        self.assertEqual(response.status_code, 204)
