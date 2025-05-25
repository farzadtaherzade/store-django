from celery import shared_task, beat
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email_order(order_id, user_mail):
    from .models import Order

    try:
        order = Order.objects.get(id=order_id)
        subject = f"Order #{order.id} Confirmation"
        message = (
            f"Hello {order.user.username},\n\n"
            f"Your order #{order.id} has been placed successfully.\n"
            f"Total amount: ${order.total_price}\n"
            f"Status: {order.get_status_display()}\n"
            f"Payment method: {order.get_method_display()}\n\n"
            "Thank you for your purchase!\n"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_mail],
            fail_silently=False,
        )
    except Order.DoesNotExist:
        pass


@shared_task
def send_payment_email(payment_id, user_mail):
    from .models import Payment

    try:
        payment = Payment.objects.get(id=payment_id)
        subject = f"Payment Confirmation for Order #{payment.order.id}"
        message = (
            f"Hello {payment.user.username},\n\n"
            f"Your payment for order #{payment.order.id} has been processed successfully.\n"
            f"Amount: ${payment.amount}\n"
            f"Status: {payment.get_status_display()}\n"
            f"Transaction ID: {payment.track_id}\n\n"
            "Thank you for your payment!\n"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_mail],
            fail_silently=False,
        )
    except Payment.DoesNotExist:
        pass


def deliver_book():
    pass
