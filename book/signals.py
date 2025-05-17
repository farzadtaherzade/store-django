from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Basket, BasketItem


@receiver(post_save, sender=BasketItem)
def update_total_price(sender, instance, created, **kwargs):
    if instance.quantity == 0:
        BasketItem.delete(instance)
        return
    instance.basket.calculate_total_price()
    print("Total price updated")
