from django.db import models
from app.models.user import User
from app.models.book import Book
from datetime import date
from django.utils import timezone
from app.models.soft_delete import SoftDeleteModel


class PurchaseBook(SoftDeleteModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchased_by = models.ForeignKey(User, related_name='purchaser', on_delete=models.CASCADE)
    date_purchased = models.DateTimeField(auto_now_add=True)
