from django.urls import path
from invoice.views import invoices, create_invoice

urlpatterns = [
    path('', invoices, name='invoices'),
    path('create', create_invoice, name='create-invoice'),
]