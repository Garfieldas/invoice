from django.urls import path
from accounts.views import dashboard, self_info, login_view, logout_view, register_view

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('settings/', self_info, name='settings'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

]