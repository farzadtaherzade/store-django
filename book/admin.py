from django.contrib import admin
from .models import Books, Review, BasketItem, Basket

# Register your models here.


@admin.register(Books)
class BookAdmin(admin.ModelAdmin):
    model = Books
    list_display = ["id", "name", "price", "tag_list"]
    # prepopulated_fields = {"slug": ["name"]}

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    model = Review


class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 1
    fields = ["book", "quantity"]


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    model = Basket
    list_display = ["id", "user", "total_price"]
    inlines = [BasketItemInline]
