from django.test import TestCase
from app.models.book import Book
from app.models.user import User
from app.models.purchase import PurchaseBook
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
import json

small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)

image = SimpleUploadedFile(name='test_image.jpg', content=small_gif,
                           content_type='image/gif')

# Create your tests here.


class PurchaseBookModelTestCase(TestCase):
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

    def test_purchasebooks_created(self):
        p1 = PurchaseBook.objects.get(id=1)
        p2 = PurchaseBook.objects.get(id=2)
        self.assertEqual(p1.book.title, "Book1")
        self.assertEqual(p2.purchased_by.first_name, "Another")
