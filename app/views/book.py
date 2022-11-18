from app.models.book import Book
from rest_framework import permissions, generics, filters
from app.serializers.book import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class AddBookView(generics.CreateAPIView):
    """Takes a set of data and creates a book"""
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = BookSerializer
    queryset = Book.objects


class RetrieveBookAPI(generics.RetrieveAPIView):
    """Returns details of a book"""

    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = BookSerializer
    lookup_field = "id"
    queryset = Book.objects


class ListBookAPI(generics.ListAPIView):
    """Returns details of all books"""
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = BookSerializer
    queryset = Book.objects.order_by('id')
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ["is_deleted", "title", "author", "date_of_pub"]
    search_fields = ("name", "book_id")


class DeleteBookAPI(generics.DestroyAPIView):
    """Delete book by id"""
    permission_classes = [permissions.IsAdminUser]
    serializer_class = BookSerializer
    queryset = Book.objects
    lookup_field = 'id'


class UpdateBookAPI(generics.UpdateAPIView):
    """Updates Book details"""

    permission_classes = [permissions.IsAdminUser]
    serializer_class = BookSerializer
    queryset = Book.objects
    lookup_field = 'id'
