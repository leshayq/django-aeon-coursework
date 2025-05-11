from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product

User = get_user_model()

class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ПІБ')
    email = models.EmailField(max_length=254, verbose_name='Електронна пошта')
    number = models.CharField(max_length=15, verbose_name='Номер телефону', blank=False, null=False)

    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Місто')
    street_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Адреса')
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name='Відділення')

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Адреса доставки'
        verbose_name_plural = 'Адреси доставки'

    def __str__(self) -> str:
        return "Shipping adress object"  + str(self.id)
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('Обробляється', 'Обробляється'),
        ('Оплачено', 'Оплачено'),
        ('Відправлено', 'Відправлено'),
        ('Доставлено', 'Доставлено'),
        ('Скасовано', 'Скасовано'),
    )
    
    DELIVERY_CHOICES = (
        ('Самовивіз', 'Самовивіз'),
        ('Кур\'єр по місту', 'Кур\'єр по місту'),
        ('Доставка у відділення', 'Доставка у відділення'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    number = models.CharField(max_length=20)
    city = models.CharField(max_length=100, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    delivery_type = models.CharField(max_length=50, choices=DELIVERY_CHOICES)
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Замовлення #{self.id}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = 'Товар в замовленні'
        verbose_name_plural = 'Товари в замовленні'
    
    def __str__(self):
        return f'{self.quantity} x {self.product.title}'
    
    def get_cost(self):
        return self.price * self.quantity