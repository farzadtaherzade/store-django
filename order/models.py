from django.db import models

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

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
