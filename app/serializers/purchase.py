from rest_framework import serializers
from app.models.purchase import PurchaseBook


class PurchaseBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseBook
        fields = '__all__'