from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart, CartItem
from base.permissions import IsCustomer


class OrderListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == "admin":
            orders = Order.objects.all().order_by("-created_at")
        else:
            orders = Order.objects.filter(user=user).order_by("-created_at")

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user

        if user.role != "customer":
            return Response({"error": "Faqat customer buyurtma bera oladi"}, status=403)

        cart, _ = Cart.objects.get_or_create(user=user)
        items = CartItem.objects.filter(cart=cart)

        if not items.exists():
            return Response({"error": "Savatcha bo‘sh"}, status=400)

        # Order yaratish
        order = Order.objects.create(user=user)

        total = 0
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            total += item.product.price * item.quantity

        order.total_price = total
        order.save()

        items.delete()  # Cartni tozalash

        return Response({"message": "Buyurtma yaratildi", "order_id": order.id})
