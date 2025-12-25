from django import forms
from invoice.models import Invoice, InvoiceItem

class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ['customer', 'due_date']


class InvoiceItemForm(forms.ModelForm):

    class Meta:
        model = InvoiceItem
        fields = ['name', 'price', 'amount', 'unit']

        