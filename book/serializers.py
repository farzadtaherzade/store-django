from rest_framework import serializers
from .models import Books, Review, BasketItem, Basket
from django.contrib.auth import get_user_model
from taggit.serializers import TagListSerializerField, TaggitSerializer
User = get_user_model()


class BooksSerializers(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Books
        fields = "__all__"
        read_only_fields = ["created", "updated", "user", "view"]


class ReviewSerializers(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    book = BooksSerializers(read_only=True)
    book = serializers.PrimaryKeyRelatedField(
        queryset=Books.objects.all(),
        write_only=True
    )

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "user"]


class BasketItemSerializers(serializers.ModelSerializer):
    quantity = serializers.IntegerField(
        min_value=1, max_value=10, default=1, required=False)

    class Meta:
        model = BasketItem
        fields = "__all__"
        read_only_fields = ["created_at", "total_price"]
