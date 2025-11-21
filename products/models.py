from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)  # zaxira
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
