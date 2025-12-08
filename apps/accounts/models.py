import uuid
from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.first_name:
            raise ValidationError('Vardas yra privalomas!')
        if not self.last_name:
            raise ValidationError('Pavardė yra privaloma!')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
