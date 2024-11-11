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
    department = models.IntegerField(blank=True, null=True, verbose_name='Відділення')

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Адреса доставки'
        verbose_name_plural = 'Адреси доставки'

    def __str__(self) -> str:
        return "Shipping adress object"  + str(self.id)
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, blank=True, null=True)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField('Сплачено', default=False)

    STATUS_CHOICES = (
    ('В обробці', 'В обробці'),
    ('Виконується', 'Виконується'),
    ('Виконано', 'Виконано'),
    ('Відмовлено', 'Відмовлено'),
    )
    status = models.CharField('Статус', max_length=100, choices=STATUS_CHOICES, default='В обробці')
    delivery_type=models.CharField('Доставка', max_length=100, default='Доставка у відділення')

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        
    def __str__(self) -> str:
        return 'Order' + str(self.id)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return 'Order item' + str(self.id)