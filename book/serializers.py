from rest_framework import serializers
from .models import Books
from django.contrib.auth import get_user_model

User = get_user_model()


class BooksSerializers(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "user"]
