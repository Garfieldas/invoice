from django.http import HttpRequest
def is_regular_user(request:HttpRequest)->bool:
    if request.user.is_superuser:
        return False
    return True