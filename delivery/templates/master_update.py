import os

files_to_update = {
    "delivery/forms.py": """from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address_from', 'address_to', 'description', 'tariff']
""",
    "delivery/views.py": """from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm

def home(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.client = request.user
            order.save()
            messages.success(request, 'Заказ успешно создан!')
            return redirect('home')
    else:
        form = OrderForm()
    return render(request, 'home.html', {'form': form})
""",
    "delivery/templates/home.html": """<!DOCTYPE html>
<html>
<head>
    <title>Создать заказ</title>
    <style>
        body { font-family: sans-serif; background: #f4f7f6; display: flex; justify-content: center; padding: 50px; }
        .form-box { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); width: 300px; }
        input, textarea, select { width: 100%; margin-bottom: 10px; padding: 8px; border: 1px solid #ccc; border-radius: 5px; }
        button { background: #28a745; color: white; border: none; padding: 10px; width: 100%; border-radius: 5px; cursor: pointer; }
        .success { color: green; margin-bottom: 15px; font-weight: bold; text-align: center; }
    </style>
</head>
<body>
    <div class="form-box">
        <h2>Новый заказ</h2>
        {% if messages %}
            {% for message in messages %}
                <div class="success">{{ message }}</div>
            {% endfor %}
        {% endif %}
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Отправить заказ</button>
        </form>
    </div>
</body>
</html>
""",
    "core/urls.py": """from django.contrib import admin
from django.urls import path
from delivery import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]
"""
}

for path, content in files_to_update.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Обновил: {path}")

print("\n--- ГОТОВО. Файлы обновлены. ---")