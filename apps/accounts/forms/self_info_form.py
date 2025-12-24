from django import forms
from accounts.models import SelfInfo

class SelfInfoForm(forms.ModelForm):
    class Meta:
        model = SelfInfo
        fields = [
            'individual_code',
            'activity_start_date',
            'address',
            'phone_number',
            'bank_name',
            'iban'
            ]
        widgets = {
            'individual_code': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'activity_start_date': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'address': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'phone_number': forms.TextInput(attrs={'class': 'input input-bordered w-full', 'type': 'tel'}),
            'bank_name': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'iban': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
        }
        label = {
            'individual_code': 'Individual code',
            'activity_start_date': 'Activity start date',
            'address': 'Address',
            'phone_number': 'Phone number',
            'bank_name': 'Bank',
            'iban': 'Bank account number'
        }