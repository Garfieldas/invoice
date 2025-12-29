from django.shortcuts import redirect
from django.contrib import messages
from apps.accounts.helpers.check_status import is_regular_user

class UserInfoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print('Active middleware for user info')

    def __call__(self, request):
        response = self.get_response(request)
        allowed_paths = ["login/", "signup/", "logout/", "/settings/"]
        response = self.get_response(request)
        if request.path in allowed_paths:
            return response
        if request.user.is_authenticated and is_regular_user(request):
            user = request.user
            if not user.has_self_info:
                messages.info(request, "Additional account information is required!")
                return redirect("settings")
        return response
            


