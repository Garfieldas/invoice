from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, UserChangeForm
from django.conf import settings
from accounts.models import User
from emailing.helpers.gmail import send_password_reset_email

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

class UpdateUserForm(UserChangeForm):
    password = None  # Exclude password field

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

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
        return (
            User.objects.filter(
                email__iexact=email,
                is_active=True
            )
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

    def get_users(self, email:str)->list[User]:
        """
        Retrieves a list of active users with usable passwords associated with the given email.
        params:email The email address to search for.
        returns: A list of User objects.
        """
        active_users = self._active_users_qs(email)
        users:list[User] = []
        for user in active_users:
            if user.has_usable_password():
                users.append(user)
        return users
    
    def save(self, *args, **kwargs)->None:
        """
        Sends a password reset email to the user.
        returns: None
        """
        email: str = self.cleaned_data["email"]
        for user in self.get_users(email):
            to_email: str = getattr(user, "email")
            if settings.ASYNC:
                send_password_reset_email.delay(to_email)
            else:
                send_password_reset_email(to_email)

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "input input-bordered w-full"
            })