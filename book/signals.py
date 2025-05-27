from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import BasketItem, Books
from .tasks import alert_stock_low


@receiver(post_save, sender=BasketItem)
def update_total_price(sender, instance, created, **kwargs):
    if instance.quantity == 0:
        BasketItem.delete(instance)
        return
    instance.basket.calculate_total_price()
    print("Total price updated")


@receiver(post_save, sender=Books)
def low_stock_notif_sellers(sender, instance, created, **kwargs):
    if created:
        return

    if instance.stock <= 5:
        print(
            f"Low stock alert for {instance.name}. Current stock: {instance.stock}")
        alert_stock_low.delay(instance.id)
