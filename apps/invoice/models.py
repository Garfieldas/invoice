from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.conf import settings
from customers.models import Customer
from decimal import Decimal

class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    invoice_number = models.PositiveIntegerField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True, help_text="Date until customer should pay")
    created_at = models.DateField(auto_now=True)

    def generate_invoice_number(self):
        """
        AutoIncrement invoice numbers according to the last one
        """
        last_invoice = (
            Invoice.objects
            .filter(user=self.user)
            .order_by('-created_at')
            .first()
        )
        if not last_invoice:
            self.invoice_number = 1
        else:
            self.invoice_number = last_invoice.invoice_number + 1

    def generate_pay_until_date(self):
        """
        If user did not selected due to date for invoice payment
        Assign 15 days from creation date
        Assign current date for created at field before model save
        """
        today = timezone.now().date()
        self.created_at = today
        self.pay_until = self.created_at + timedelta(days=15)

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.generate_pay_until_date()
        self.generate_invoice_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.full_name} - {self.invoice_number} - {self.created_at}"
    

class InvoiceItem(models.Model):
    UNITS=(
        ('HOURS', 'val'),
        ('AMOUNT', 'vnt')
    )
    name = models.CharField(max_length=250, blank=False)
    price = models.DecimalField(max_digits=3, decimal_places=2, help_text="Price per unit")
    amount = models.PositiveIntegerField(blank=False)
    unit = models.CharField(choices=UNITS, max_length=10, blank=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_items')

    def __str__(self):
        return f"{self.name} - {self.price} - {self.unit}"
