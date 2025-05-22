from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from book.models import Basket, BasketItem
from .models import Order, OrderItem
from .serializers import OrderSerializers
from django.core.mail import send_mail

# Create your views here.


class CheckoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializers

    def post(self, request):
        user = request.user
        basket = Basket.objects.get(user=user)
        basket_items = BasketItem.objects.filter(basket=basket, is_ghost=False)
        basket.calculate_total_price()

        if not basket_items.exists():
            return Response({"message": "Your basket is empty"}, status=400)

        order = Order.objects.create(
            user=user,
            total_price=basket.total_price,
            status="pending",
            method=request.data.get("method", "online_payment"),
        )

        for item in basket_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.get_total_price(),
            )

        # basket_items.filter(is_ghost=False).delete()
        serializer = self.get_serializer(order)
        send_mail(
            subject="Order Confirmation",
            message=f"Your order #{order.id} has been placed successfully. Total amount: ${order.total_price}",
            from_email="",
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response(serializer.data, status=201)


class OrderList(ListAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializers
    filter_backends = [OrderingFilter]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
