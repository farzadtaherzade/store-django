from .models import Order, OrderItem
from rest_framework import serializers
from book.serializers import BooksSerializers


class OrderItemSerializers(serializers.ModelSerializer):
    book = BooksSerializers(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ["id", "order", "book", "price"]


class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializers(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at",
                            "user", "total_price", "status", "will_deliver_time"]
