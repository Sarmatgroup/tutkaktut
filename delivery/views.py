import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.utils import timezone
from .models import Order, Tariff

def home(request):
    if request.method == 'POST':
        address_from = request.POST.get('address_from')
        address_to = request.POST.get('address_to')
        tariff_id = request.POST.get('tariff_id')
        distance = float(request.POST.get('distance', 0))
        phone = request.POST.get('client_phone')
        comment = request.POST.get('comment')

        try:
            tariff = Tariff.objects.get(id=tariff_id)
            calculated_price = (distance * float(tariff.price_per_km)) + float(tariff.base_price)

            order = Order.objects.create(
                client=request.user if request.user.is_authenticated else None,
                address_from=address_from,
                address_to=address_to,
                tariff=tariff,
                distance=distance,
                final_price=calculated_price,
                client_phone=phone,
                comment=comment,
                status='searching'
            )
            return JsonResponse({'status': 'success', 'order_id': order.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    tariffs = Tariff.objects.all()
    return render(request, 'home.html', {'tariffs': tariffs})

def get_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return JsonResponse({'status': order.status})

# Главная страница курьера (теперь просто отдает пустой шаблон с картой)
def courier_dashboard(request):
    return render(request, 'courier.html')

# Эндпоинт: отдает список заказов, которые ищут курьера
def get_available_orders(request):
    orders = Order.objects.filter(status='searching').order_by('-id')
    orders_data = [{
        'id': o.id,
        'address_from': o.address_from,
        'address_to': o.address_to,
        # Если final_price равен None, возьмется 0, и сервер не упадет
        'final_price': float(o.final_price or 0), 
        'comment': o.comment or ''
    } for o in orders]
    return JsonResponse({'orders': orders_data})

# Эндпоинт: считает баланс курьера и отдает историю выполненных заказов
def get_courier_history(request):
    completed_orders = Order.objects.filter(status='completed').order_by('-id')
    
    total_balance = completed_orders.aggregate(Sum('final_price'))['final_price__sum'] or 0
    
    history_data = [{
        'id': o.id,
        'address_from': o.address_from[:300],
        'address_to': o.address_to[:300],
        'final_price': float(o.final_price or 0), # Безопасный фикс здесь тоже
    } for o in completed_orders]
    
    return JsonResponse({
        'balance': float(total_balance),
        'history': history_data
    })
    
    return JsonResponse({
        'balance': float(total_balance),
        'history': history_data
    })

@csrf_exempt
def update_status(request, order_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_status = data.get('status')
        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            return JsonResponse({'status': 'success'})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Заказ не найден'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Неверный метод'}, status=400)