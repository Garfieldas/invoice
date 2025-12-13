from django.urls import path
from accounts.views import dashboard, self_info

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('settings/', self_info, name='settings'),
]