from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Экран клиента
    path('courier/', views.courier_dashboard, name='courier_dashboard'),  # Экран курьера
    path('courier/available-orders/', views.get_available_orders, name='get_available_orders'),  # Получение новых заказов (JSON)
    path('courier/history/', views.get_courier_history, name='get_courier_history'),  # История и баланс (JSON)
    path('order/<int:order_id>/update/', views.update_status, name='update_status'),  # Изменение статуса заказа
    path('order/<int:order_id>/status/', views.get_status, name='get_status'),  # Статус заказа для клиента
]