from django.urls import path
from customers.views import customers, customer_details, delete_customer, create_customer

urlpatterns = [
    path('', customers, name='customers'),
    path('customer/create', create_customer, name='customer_create'),
    path('customer/<int:customer_pk>', customer_details, name='customer_details'),
    path('customer/delete/<int:customer_pk>', delete_customer, name='customer_delete'),
]