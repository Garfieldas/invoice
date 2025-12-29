from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from apps.accounts.helpers.check_status import is_regular_user

class UserInfoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print('Active middleware for user info')

    def __call__(self, request):
        allowed_paths = [reverse("login"), reverse("register"), reverse("logout"), reverse("settings")]
        if request.path in allowed_paths:
            return self.get_response(request)
        if request.user.is_authenticated and is_regular_user(request):
            user = request.user
            if not user.has_self_info:
                messages.info(request, "Additional account information is required!")
                return redirect("settings")
        return self.get_response(request)
            


