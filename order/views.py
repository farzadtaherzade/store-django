from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from book.models import Basket, BasketItem
from .models import Order, OrderItem
from .serializers import OrderSerializers

# Create your views here.


class CheckoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializers

    def post(self, request):
        user = request.user
        basket = Basket.objects.get(user=user)
        basket_items = BasketItem.objects.filter(basket=basket)
        basket.calculate_total_price()

        if not basket_items.exists():
            return Response({"message": "Your basket is empty"}, status=400)

        order = Order.objects.create(
            user=user,
            total_price=basket.calculate_total_price(),
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

        basket_items.delete()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=201)
