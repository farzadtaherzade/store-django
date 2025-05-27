from django.conf import settings
from .models import Books
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def decrease_stock(book_id, quantity):
    try:
        book = Books.objects.get(id=book_id)

        book.stock -= quantity
        book.save()

    except Books.DoesNotExist:
        pass


@shared_task
def alert_stock_low(book_id):
    try:
        book = Books.objects.get(id=book_id)
        print(f"Sending low stock alert")
        send_mail(
            subject='Low Stock Alert',
            message=f'The stock for {book.name} is low. Current stock: {book.stock}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[book.user.email],
            fail_silently=False,
        )
    except Books.DoesNotExist:
        pass
