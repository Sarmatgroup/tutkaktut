from django.db import models
from django.contrib.auth.models import User

# Модель Тарифов
class Tariff(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название тарифа (например, Экспресс)")
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за 1 км (руб)")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Базовая стоимость (посадка)")
    is_active = models.BooleanField(default=True, verbose_name="Тариф доступен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"


# Обновленная модель Заказа
class Order(models.Model):
    # Жестко заданные статусы из твоего ТЗ
    STATUS_CHOICES = [
        ('searching', 'Поиск курьера'),
        ('on_way', 'Курьер в пути'),
        ('delivering', 'Курьер везет Ваш заказ'),
        ('delivered', 'Заказ доставлен'),
        ('canceled', 'Отменен'),
    ]

    # Связи с пользователями
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_orders', verbose_name="Клиент", null=True, blank=True)
    courier = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='courier_orders', verbose_name="Курьер", null=True, blank=True)

    # Логистика
    address_from = models.CharField(max_length=256, verbose_name="Откуда")
    address_to = models.CharField(max_length=255, verbose_name="Куда")
    distance = models.FloatField(verbose_name="Расстояние (км)", null=True, blank=True)
    
    # Тариф и деньги
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True, verbose_name="Выбранный тариф")
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая стоимость", null=True, blank=True)
    
    # Дополнительные данные от клиента
    client_phone = models.CharField(max_length=20, verbose_name="Телефон клиента", blank=True)
    comment = models.TextField(verbose_name="Комментарий курьеру", blank=True)

    # Системное
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='searching', verbose_name="Статус заказа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")

    def __str__(self):
        return f"Заказ #{self.id} | {self.address_from} -> {self.address_to} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"