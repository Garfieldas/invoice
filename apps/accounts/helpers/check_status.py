from django.http import HttpRequest
def check_status(request:HttpRequest)->bool:
    if request.user.is_superuser:
        return False
    return False