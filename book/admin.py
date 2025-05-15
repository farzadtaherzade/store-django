from django.contrib import admin
from .models import Books

# Register your models here.


@admin.register(Books)
class BookAdmin(admin.ModelAdmin):
    model = Books
    # prepopulated_fields = {"slug": ["name"]}
