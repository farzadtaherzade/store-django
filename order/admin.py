from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "status", "created_at")
    search_fields = ("user__username", "user__email")
    list_filter = ("status",)
    ordering = ("-created_at",)
    list_per_page = 10
    date_hierarchy = "created_at"
    raw_id_fields = ("user",)
