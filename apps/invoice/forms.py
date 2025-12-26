from django import forms
from django.forms import inlineformset_factory
from invoice.models import Invoice, InvoiceItem

class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ['customer', 'due_date']

        widgets = {
            'customer': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'due_date': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
        }

    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance



class InvoiceItemForm(forms.ModelForm):

    class Meta:
        model = InvoiceItem
        fields = ['name', 'price', 'amount', 'unit']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'price': forms.NumberInput(attrs={'class': 'input input-bordered w-full', 'type': 'number'}),
            'amount': forms.NumberInput(attrs={'class': 'input input-bordered w-full', 'type': 'number'}),    
            'unit': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }

    def __init__(self, *args, **kwargs):
        invoice = kwargs.pop('invoice', None)
        super().__init__(*args, **kwargs)
        self.invoice = invoice

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.invoice:
            instance.invoice = self.invoice
        elif getattr(self.instance, "invoice", None):
            instance.invoice = self.instance.invoice
        if commit:
            instance.save()
        return instance
    
InvoiceItemFormset = inlineformset_factory(
    parent_model=Invoice,
    model=InvoiceItem,
    form = InvoiceItemForm,
    extra = 1,
    can_delete=True
)
