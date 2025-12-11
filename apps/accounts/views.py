from django.shortcuts import render

def user_settings(request):
    return render(request, 'accounts/user_settings.html')
