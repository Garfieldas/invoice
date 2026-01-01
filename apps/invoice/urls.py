from django.urls import path
from django.conf import settings
from invoice.views import( 
invoices, create_invoice, invoice_details,
delete_invoice, create_invoice_pdf
)

urlpatterns = [
    path('', invoices, name='invoices'),
    path('create', create_invoice, name='create-invoice'),
    path('details/<int:invoice_pk>', invoice_details, name='invoice-details'),
    path('delete/<int:invoice_pk>', delete_invoice, name='invoice_delete'),
    path('pdf/<int:invoice_pk>', create_invoice_pdf, name='invoice_pdf'),
]
