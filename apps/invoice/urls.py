from django.urls import path
from invoice.views import invoices, create_invoice, add_new_invoice_item

urlpatterns = [
    path('', invoices, name='invoices'),
    path('create', create_invoice, name='create-invoice'),
    path('add_invoice_item', add_new_invoice_item, name='add-invoice-item'),

]