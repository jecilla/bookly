from django.db import models
from datetime import date
from gdstorage.storage import GoogleDriveStorage
from django.core.validators import MaxValueValidator, MinValueValidator
from app.models.soft_delete import SoftDeleteModel

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

class Book(SoftDeleteModel):
    title = models.CharField(max_length=100)
    book_cover = models.ImageField(upload_to = 'uploads/', storage=gd_storage, blank = True,null=True)
    author = models.CharField(max_length=100)
    date_of_pub = models.DateField(default=date.today)
    number_of_pages = models.IntegerField(validators=[
            MaxValueValidator(1000),
            MinValueValidator(1)
        ])
    number_of_books = models.IntegerField(default = 0,validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])

    def __str__(self) -> str:
        return self.title