from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import api_view
from book.models import Basket, BasketItem
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializers
from .tasks import send_email_order, send_payment_email
import requests as req

# Create your views here.


class CheckoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializers

    def post(self, request):
        user = request.user

        try:
            basket = Basket.objects.get(user=user)
            basket_items = BasketItem.objects.filter(
                basket=basket, is_ghost=False)
            basket.calculate_total_price()

            if not basket_items.exists():
                return Response({"message": "Your basket is empty"}, status=400)

            # Create order
            order = Order.objects.create(
                user=user,
                total_price=basket.total_price,
                status="pending",
                method=request.data.get("method", "online_payment"),
            )

            # Create order items
            for item in basket_items:
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.get_total_price(),
                )

            serializer = self.get_serializer(order)
            send_email_order(order.id, user.email)

            # Payment gateway integration
            try:
                # Convert to smallest currency unit
                amount = int(order.total_price * 100)

                response = req.post(
                    "https://gateway.zibal.ir/v1/request",
                    json={
                        "merchant": "zibal",  # Should be your actual merchant ID
                        "amount": amount,
                        "callbackUrl": "http://localhost:8000/api/checkout/callback/",
                    },
                    timeout=10
                )

                response.raise_for_status()
                data = response.json()

                # Validate the response contains trackId
                if 'trackId' not in data:
                    raise ValueError("Missing trackId in gateway response")

                track_id = data['trackId']

            except Exception as e:
                # If payment fails, mark order as failed but don't create payment record
                order.status = 'failed'
                order.save()
                return Response({
                    "message": "Payment gateway error",
                    "error": str(e),
                    "response_data": data if 'data' in locals() else None
                }, status=500)

            # Only create payment if we have a valid track_id
            payment = Payment.objects.create(
                order=order,
                user=user,
                amount=order.total_price,
                track_id=track_id,  # Now guaranteed to have value
                status="pending",
            )

            return Response({
                "data": serializer.data,
                "payment_url": f"https://gateway.zibal.ir/start/{track_id}",
            }, status=201)

        except Basket.DoesNotExist:
            return Response({"message": "Basket not found"}, status=400)


class OrderList(ListAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializers
    filter_backends = [OrderingFilter]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)


@api_view(["GET"])
def payment_callback(request):
    url = "https://gateway.zibal.ir/v1/verify"
    success = request.GET["success"]
    trackid = request.GET["trackId"]
    status = request.GET["status"]

    try:
        payment = Payment.objects.get(track_id=trackid, status="pending")
    except Payment.DoesNotExist:
        return Response({"message": "Payment not found"}, status=404)

    print(status)

    if status == "2" and success == "1":
        res = req.post(
            url,
            json={
                "merchant": "zibal",
                "trackId": payment.track_id
            }
        )

        data = res.json()
        print(data)

        if data.get("result") == 100:
            payment.status = "success"
            payment.result = data.get("result")
            payment.ref_number = data.get("refNumber")
            payment.paid_at = data.get("paidAt")
            payment.save()
        else:
            payment.status = "failed"
            payment.result = data.get("result")
            payment.save()

    send_payment_email(payment.id, payment.user.email)
    return Response({"message": "payment was successfuly", "success": success, "status": status}, status=200)
