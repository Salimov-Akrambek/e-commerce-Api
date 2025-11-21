from django.db import models
from orders.models import Order   # <-- SHU JOY ETISHMAGAN


class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Kutilmoqda'),
        ('paid', 'To‘landi'),
        ('failed', 'Xato'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=50, default='card')   # karta/payme/click...
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} — {self.order.id} ({self.status})"
