from django.urls import path
from .views import CreatePaymentView, ConfirmPaymentView, PaymentListView

urlpatterns = [
    path('payments/', PaymentListView.as_view()),
    path('payments/create/', CreatePaymentView.as_view()),
    path('payments/confirm/<int:payment_id>/', ConfirmPaymentView.as_view()),
]
