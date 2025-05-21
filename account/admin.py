from django.contrib import admin
from .models import Profile, Address

# Register your models here.


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # model = Profile
    list_display = ("user", "avatar")
    search_fields = ("user__username", "user__email")
    list_filter = ("user__is_active",)
    ordering = ("user__username",)
    list_per_page = 10
    inlines = [AddressInline]
