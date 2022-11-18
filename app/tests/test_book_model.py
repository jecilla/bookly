from django.test import TestCase
from app.models.book import Book
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


class BookTestCase(TestCase):
    def setUp(self):
        self.image = json.dumps(str(''))
        Book.objects.create(
            title="Book1",
            book_cover=self.image,
            author="Jovc",
            date_of_pub=timezone.now(),
            number_of_pages=44,
            number_of_books=4
        )
        Book.objects.create(
            title="Book2",
            book_cover=self.image,
            author="Lori",
            date_of_pub=timezone.now(),
            number_of_pages=44,
            number_of_books=4
        )

    def test_book_created(self):
        book1 = Book.objects.get(title="Book1")
        book2 = Book.objects.get(title="Book2")
        self.assertEqual(book1.author, "Jovc")
        self.assertEqual(book2.author, "Lori")
