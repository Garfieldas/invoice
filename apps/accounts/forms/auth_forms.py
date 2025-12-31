from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
from accounts.models import User
from emailing.helpers.gmail import send_password_reset_email
from django.contrib.auth.tokens import default_token_generator

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

class ResetPasswordForm(forms.Form):

    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'class': 'input input-bordered w-full', 'placeholder': 'Email'}),
    )

    def _active_users_qs(self, email):
        """
        Returns a queryset of active users with the given email.
        params: email: The email address to filter users by.
        returns: QuerySet of active users with the given email."""
        email_field_name = User.get_email_field_name()
        return User._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                "is_active": True,
            }
        )

    def clean_email(self):
        """
        Validates that there is at least one active user associated with the given email.
        returns: The cleaned email if valid.
        raises: ValidationError if no active user is found.
        """
        email = self.cleaned_data.get("email")
        qs = self._active_users_qs(email)
        if not qs.exists():
            raise forms.ValidationError("There is no active user associated with this email address.")
        return email

    def get_users(self, email):
        """
        Given an email, return matching user(s) who should receive a reset.
        params: email: The email address to filter users by.
        returns: Generator of users who should receive a password reset.
        """
        active_users = self._active_users_qs(email)
        return (user for user in active_users if user.has_usable_password())
    
    def save(self, *args, **kwargs)->None:
        """
        Sends a password reset email to the user.
        returns: None
        """
        email: str = self.cleaned_data["email"]
        email_field_name: str = User.get_email_field_name()
        for user in self.get_users(email):
            user_email: str = getattr(user, email_field_name)
            user_pk_bytes = force_bytes(User._meta.pk.value_to_string(user))
            uidb64 = urlsafe_base64_encode(user_pk_bytes)
            token = default_token_generator.make_token(user)
            password_reset_link: str = f"{settings.BASE_URL}{reverse('password_reset_confirm', args=[uidb64, token])}"
            if settings.ASYNC:
                send_password_reset_email.delay(user_email, password_reset_link)
            else:
                send_password_reset_email(user_email, password_reset_link)

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "input input-bordered w-full"
            })