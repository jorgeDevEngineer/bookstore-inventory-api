from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        # Evitamos que el usuario asigne estos valores manualmente en un POST o PUT
        read_only_fields = ['created_at', 'updated_at', 'selling_price_local']