from django.conf import settings
from .models import Cart, CartItem
from decimal import Decimal
from django.utils import timezone

class CartManager:
    def __init__(self, request):
        """Initialize the cart"""
        self.session = request.session
        self.user = request.user if request.user.is_authenticated else None
        
        # Try to get cart from database
        cart_id = self.session.get('cart_id')
        if self.user:
            # Logged in user - get or create their cart
            cart = Cart.objects.filter(user=self.user).first()
            if cart:
                self.cart = cart
                self.session['cart_id'] = cart.id
            elif cart_id:
                # Try to associate existing session cart with user
                try:
                    cart = Cart.objects.get(id=cart_id)
                    cart.user = self.user
                    cart.save()
                    self.cart = cart
                except Cart.DoesNotExist:
                    self.cart = self._create_cart()
            else:
                self.cart = self._create_cart()
        else:
            # Anonymous user
            if cart_id:
                try:
                    self.cart = Cart.objects.get(id=cart_id)
                except Cart.DoesNotExist:
                    self.cart = self._create_cart()
            else:
                self.cart = self._create_cart()
    
    def _create_cart(self):
        """Create a new cart"""
        if self.user:
            cart = Cart.objects.create(user=self.user)
        else:
            cart = Cart.objects.create(session_id=self.session.session_key)
        self.session['cart_id'] = cart.id
        return cart
    
    def add(self, product, quantity=1, update_quantity=False):
        """Add a product to cart or update its quantity"""
        try:
            cart_item = CartItem.objects.get(cart=self.cart, product=product)
            if update_quantity:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(cart=self.cart, product=product, quantity=quantity)
        
        self.cart.updated_at = timezone.now()
        self.cart.save()
    
    def remove(self, product):
        """Remove a product from cart"""
        try:
            cart_item = CartItem.objects.get(cart=self.cart, product=product)
            cart_item.delete()
            self.cart.updated_at = timezone.now()
            self.cart.save()
        except CartItem.DoesNotExist:
            pass
    
    def get_items(self):
        """Get all items in cart"""
        return self.cart.items.all()
    
    def get_total_price(self):
        """Get total price of all items in cart"""
        return self.cart.get_total_price()
    
    def get_total_items(self):
        """Get total number of items in cart"""
        return self.cart.get_total_items()
    
    def clear(self):
        """Clear the cart"""
        self.cart.clear()
