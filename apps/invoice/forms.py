from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from invoice.models import Invoice, InvoiceItem, Customer

class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ['customer', 'due_date']

        widgets = {
            'customer': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'due_date': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
        }

    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(provider=self.user)

    def clean_customer(self):
        customer = self.cleaned_data.get('customer', None)
        if not customer:
            raise ValidationError('customer is required!')
        return customer

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
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
        self.invoice = kwargs.pop('invoice', None)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
    
InvoiceItemFormset = inlineformset_factory(
    parent_model=Invoice,
    model=InvoiceItem,
    form = InvoiceItemForm,
    extra = 2,
    min_num=1,
    can_delete=True,
    validate_min=True,
)
