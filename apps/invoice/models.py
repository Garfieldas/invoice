from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.conf import settings
from customers.models import Customer
from decimal import Decimal

class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    invoice_number = models.PositiveIntegerField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True, help_text="Date until customer should pay")
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_invoice_number(self):
        """
        AutoIncrement invoice numbers according to the last one
        """
        if self.invoice_number:
            return
        last_invoice = (
            Invoice.objects
            .filter(user=self.user)
            .order_by('-invoice_number')
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
        if self.due_date:
            return
        today = timezone.now().date()
        self.due_date = today + timedelta(days=15)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.generate_pay_until_date()
            self.generate_invoice_number()
        super().save(*args, **kwargs)

    @property
    def invoice_number_display(self):
        return str(self.invoice_number).zfill(6)

    def __str__(self):
        return f"{self.user.full_name} - {self.invoice_number}"
    

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

    @property
    def total_price(self):
        return self.price * self.amount

    def __str__(self):
        return f"{self.name} - {self.price} - {self.unit}"
