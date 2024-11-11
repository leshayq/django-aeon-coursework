from django import forms
from .models import ContactRequest

class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactRequest
        fields = ('name', 'contact_info', 'subject', 'message')
        exclude = ('created_at',)