from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'method', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']
