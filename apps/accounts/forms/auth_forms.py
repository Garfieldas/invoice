from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from accounts.models import User

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Password'})
    )

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "input input-bordered w-full"
            })

class ResetPasswordForm(PasswordResetForm):

    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'class': 'input input-bordered w-full', 'placeholder': 'Email'}),
    )
