from app.models.purchase import PurchaseBook
from rest_framework import permissions, generics, filters
from app.serializers.purchase import PurchaseBookSerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class AddPurchaseBookView(generics.CreateAPIView):
    """Takes a set of data and creates a PurchaseBook"""
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = PurchaseBookSerializer
    queryset = PurchaseBook.objects


class RetrievePurchaseBookAPI(generics.RetrieveAPIView):
    """Returns details of a PurchaseBook"""

    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = PurchaseBookSerializer
    lookup_field = "id"
    queryset = PurchaseBook.objects


class ListPurchaseBookAPI(generics.ListAPIView):
    """Returns details of all PurchaseBooks"""
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = PurchaseBookSerializer
    queryset = PurchaseBook.objects.order_by('id')
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ["is_deleted", "book", "purchased_by"]
    search_fields = ("book", "purchased_by")


class DeletePurchaseBookAPI(generics.DestroyAPIView):
    """Delete PurchaseBook by id"""
    permission_classes = [permissions.IsAdminUser]
    serializer_class = PurchaseBookSerializer
    queryset = PurchaseBook.objects
    lookup_field = 'id'


class UpdatePurchaseBookAPI(generics.UpdateAPIView):
    """Updates PurchaseBook details"""

    permission_classes = [permissions.IsAdminUser]
    serializer_class = PurchaseBookSerializer
    queryset = PurchaseBook.objects
    lookup_field = 'id'
