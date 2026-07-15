from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address_from', 'address_to']
        widgets = {
            'address_from': forms.TextInput(attrs={'placeholder': 'Адрес отправления', 'id': 'id_addr_from', 'readonly': 'readonly'}),
            'address_to': forms.TextInput(attrs={'placeholder': 'Адрес доставки', 'id': 'id_addr_to', 'readonly': 'readonly'}),
        }