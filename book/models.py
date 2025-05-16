from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Books(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    edition = models.IntegerField(default=1)
    language = models.CharField()
    cover = models.ImageField(upload_to="books/")
    page_count = models.PositiveBigIntegerField()
    stock = models.PositiveIntegerField(default=0)
    tags = TaggableManager()
    author = models.CharField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="books")
    is_active = models.BooleanField(default=True)
    view = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Book"

    def __str__(self):
        return self.name


class Review(models.Model):
    book = models.ForeignKey(
        Books, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("book", "user")

    def __str__(self):
        return f"{self.user.username} - {self.book.name} - {self.rating}"
