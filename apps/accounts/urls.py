from django.urls import path
from accounts.views import (
    dashboard,
    self_info,
    register_view,
    login_view,
    logout_view,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    UpdateUserView,
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('settings/', self_info, name='settings'),
    path('update-profile/', UpdateUserView.as_view(), name='update_profile'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]