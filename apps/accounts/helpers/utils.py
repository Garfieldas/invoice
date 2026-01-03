from typing import Optional
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.urls import reverse
from accounts.models import User

def create_password_reset_link(user:User)->str:
    user_pk_bytes:bytes = force_bytes(User._meta.pk.value_to_string(user))
    uidb64: str = urlsafe_base64_encode(user_pk_bytes)
    token: str = default_token_generator.make_token(user)
    password_reset_link: str = f"{settings.BASE_URL}{reverse('password_reset_confirm', args=[uidb64, token])}"
    return password_reset_link



