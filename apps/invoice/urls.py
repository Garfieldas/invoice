from django.urls import path
from invoice.views import invoices, create_invoice, invoice_details, delete_invoice

urlpatterns = [
    path('', invoices, name='invoices'),
    path('create', create_invoice, name='create-invoice'),
    path('invoice/<int:invoice_pk>', invoice_details, name='invoice-details'),
    path('invoice/delete/<int:invoice_pk>', delete_invoice, name='invoice_delete'),

]