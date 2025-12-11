from django.shortcuts import render

def dashboard(request):
    return render(request, 'accounts/user_settings.html')
