from .models import Order, OrderItem
from rest_framework import serializers


class OrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["id", "user", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at", "user"]
