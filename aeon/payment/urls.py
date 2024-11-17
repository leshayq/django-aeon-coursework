from . import views
from django.urls import path
from .views import PayView, PayCallbackView

app_name = 'payment'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_fail/', views.payment_fail, name='payment_fail'),
    path('payment/', PayView.as_view(), name='payment'),
    path('payment/callback/', PayCallbackView.as_view(), name='payment_callback'),
]