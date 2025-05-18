from django.shortcuts import redirect
from django.urls import reverse

class FirstLoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.first_login and request.path != reverse('change-password'):
                return redirect('change-password')
        return self.get_response(request)
