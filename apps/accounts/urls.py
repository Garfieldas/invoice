from django.urls import path
from accounts.views import (
    dashboard,
    self_info,
    register_view,
    login_view,
    logout_view,
    CustomPasswordResetView,
    CustomPasswordResetDoneView
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('settings/', self_info, name='settings'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),

]