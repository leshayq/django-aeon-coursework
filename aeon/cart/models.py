from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product

User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзини'
    
    def __str__(self):
        return f"Корзина {'користувача ' + self.user.username if self.user else 'гостя'}"
    
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    def clear(self):
        self.items.all().delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = 'Товар в корзині'
        verbose_name_plural = 'Товари в корзині'
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
    
    def get_cost(self):
        return self.product.price * self.quantity