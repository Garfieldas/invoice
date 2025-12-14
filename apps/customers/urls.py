from django.urls import path
from customers.views import customers

urlpatterns = [
    path('', customers, name='customers'),
]