from django.urls import path
from accounts.views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
]