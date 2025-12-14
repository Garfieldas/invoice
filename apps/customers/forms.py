from django import forms
from customers.models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'company_name', 'company_code', 'vat_code', 'address', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'company_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'company_code': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'vat_code': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'address': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'phone_number': forms.TelInput(attrs={'class': 'input input-bordered w-full', 'type': 'tel'}),
        }

    def __init__(self, *args, **kwargs):
        provider = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.provider = provider