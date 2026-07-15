import os

# Создаем структуру файлов
files = {
    "delivery/views.py": """from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
""",
    "core/urls.py": """from django.contrib import admin
from django.urls import path
from delivery import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
]
""",
    "delivery/templates/home.html": """<!DOCTYPE html>
<html>
<head><title>Мой Сервис</title></head>
<body>
    <h1>Привет! Это твой сервис доставки</h1>
    <p>Мы только что автоматически создали эту страницу.</p>
</body>
</html>
"""
}

# Создаем папку для шаблонов, если ее нет
os.makedirs("delivery/templates", exist_ok=True)

# Записываем контент в файлы
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Файл {path} создан/обновлен.")

print("\n--- ВСЕ ГОТОВО! ---")
print("Теперь запусти в терминале: python manage.py runserver")