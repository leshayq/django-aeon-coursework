from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'email', 'number', 'city', 'street_address', 'department']
        exclude = ('user',)