from django.shortcuts import redirect
from django.conf import settings

class GlobalPasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Если пользователь уже авторизован паролем или находится на странице логина — пропускаем
        if request.session.get('site_access') or request.path == '/login-gate/':
            return self.get_response(request)
        
        return redirect('/login-gate/')