import uuid
from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.first_name:
            raise ValidationError('Vardas yra privalomas!')
        if not self.last_name:
            raise ValidationError('Pavardė yra privaloma!')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    
class SelfInfo(models.Model):

    BANK_CHOICES = (
        ("SWEDBANK", "Swedbank"),
        ("SEB", "Seb"),
        ("CITADELE", "Citadele"),
        ("LUMINOR", "Luminor"),
        ("ARTEA", "ARTEA"),
        ("REVOLUT", "Revolut")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='self_info')
    individual_code = models.CharField(max_length=255, blank=False)
    activity_start_date = models.DateField(null=True, blank=True, help_text="Activity start date")
    address = models.CharField(max_length=255, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    bank_name = models.CharField(choices=BANK_CHOICES, max_length=50, blank=False)
    iban = models.CharField(max_length=50, blank=False)
    
    def __str__(self):
        return f"{self.individual_code} {self.address}"
