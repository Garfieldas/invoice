from django.urls import path
from accounts.views import user_settings

urlpatterns = [
    path('information', user_settings, name='settings'),
]