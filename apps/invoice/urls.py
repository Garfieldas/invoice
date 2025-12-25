from django.urls import path
from invoice.views import invoices

urlpatterns = [
    path('', invoices, name='invoices'),
]