from django.shortcuts import redirect
from django.contrib import messages
from apps.accounts.helpers.check_status import check_status

class UserInfoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print('Active middleware for user info')

    def __call__(self, request):
        if request.user.is_authenticated and check_status(request):
            user = request.user
            if not user.has_self_info:
                messages.info(request, "Additional account information is required!")
                return redirect("settings")
        response = self.get_response(request)
        return response
            


