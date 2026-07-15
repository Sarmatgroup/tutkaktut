# Файл: delivery/admin.py
from django.contrib import admin
from .models import Order, Tariff

admin.site.register(Order)
admin.site.register(Tariff)