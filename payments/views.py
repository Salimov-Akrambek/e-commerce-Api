class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        method = request.data.get('method', 'card')

 #  o'z buyurtmasi
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Buyurtma topilmadi"}, status=404)

        # Payment 
        if hasattr(order, 'payment'):
            return Response({"error": "Bu buyurtma uchun allaqachon to‘lov mavjud"}, status=400)

        payment = Payment.objects.create(
            order=order,
            amount=order.total_price,
            method=method
        )

        return Response(PaymentSerializer(payment).data, status=201)

# tasdiqlash
class ConfirmPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id, order__user=request.user)
        except Payment.DoesNotExist:
            return Response({"error": "To‘lov topilmadi"}, status=404)

        payment.status = 'paid'
        payment.save()

        return Response({"message": "To‘lov tasdiqlandi!"})

        
# royxati
class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)

