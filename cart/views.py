from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer
from base.permissions import IsCustomer


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Mahsulot topilmadi"}, status=404)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return Response({"message": "Savatchaga qo‘shildi"})

    def delete(self, request):
        item_id = request.data.get("item_id")

        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Item topilmadi"}, status=404)

        item.delete()
        return Response({"message": "O‘chirildi"})
