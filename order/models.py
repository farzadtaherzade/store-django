from django.db import models
from django.contrib.auth import get_user_model
from book.models import Books

# Create your models here.

User = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    METHOD_CHOICES = [
        ("online_payment", "Online Payment"),
        ("chash_on_delivery", "Cash on Delivery"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending")
    method = models.CharField(
        max_length=20, choices=METHOD_CHOICES, default="online_payment")

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def calculate_total_price(self):
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_price = total
        self.save()
        return


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey("book.Books", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.book.name}"

    def get_total_price(self):
        return self.quantity * self.price


class Payment(models.Model):
    STATUS_CHOICES = (
        ("process", "Process"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="payments"
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments"
    )

    track_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="process"
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    ref_number = models.IntegerField(null=True, blank=True)
    result = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"
