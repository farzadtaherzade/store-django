from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_order(order, user_mail):
    send_mail(
        subject="Order Confirmation",
        message=f"Your order #{order.id} has been placed successfully. Total amount: ${order.total_price}",
        from_email="",
        recipient_list=[user_mail],
        fail_silently=False,
    )
