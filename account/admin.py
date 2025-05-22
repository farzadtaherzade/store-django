from django.contrib import admin
from .models import Profile, Address
from django.utils.html import format_html

# Register your models here.


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    fields = ("address", "zip_code", "pelak")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ("id", "user", "show_avatar")
    search_fields = ("user__username", "user__email")
    list_filter = ("user__is_active",)
    ordering = ("user__username",)
    list_per_page = 10
    inlines = [AddressInline]

    def show_avatar(self, obj):
        if obj.avatar:
            return format_html(
                f"<img src='{obj.avatar.url}' alt='{obj.user.username}' style='width: 50px; height: 50px; border-radius: 50%;' />"
            )
        return "No Avatar"
