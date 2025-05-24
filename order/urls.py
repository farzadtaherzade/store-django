from django.urls import path
from . import views

urlpatterns = [
    path("", views.CheckoutView.as_view(), name="checkout"),
    path("order-history/", views.OrderList.as_view(), name="order-history"),
    path("callback/", views.payment_callback, name="payment-callback"),
]
