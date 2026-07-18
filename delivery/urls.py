from django.urls import path
from . import views # Импортируем все вьюхи из твоего файла views.py

urlpatterns = [
    # твой путь для главной
    path('', views.home, name='home'),
    path('courier/', views.courier_dashboard, name='courier'), 
    # путь для входа
    path('login-gate/', views.login_gate_view, name='login_gate'),
]