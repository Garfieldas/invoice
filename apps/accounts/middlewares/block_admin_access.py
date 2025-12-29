from django.urls import reverse
from django.shortcuts import redirect
from accounts.helpers.check_status import is_regular_user

class BlockAdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print('Admin restriction middleware is active!')

    def __call__(self, request):
        admin_url = reverse("admin:index")
        if request.path != admin_url:
            return self.get_response(request)
        
        if not request.user.is_authenticated:
            return redirect("login")
        
        if is_regular_user(request):
            return redirect("dashboard")
        
        return self.get_response(request)