from django.db import models
from accounts.models import User

class Customer(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients', null=True)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    company_name = models.CharField(max_length=255, blank=False)
    company_code = models.CharField(max_length=50, unique=True, blank=False)
    vat_code = models.CharField(max_length=50, blank=False)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.company_name
