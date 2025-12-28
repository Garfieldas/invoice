from typing import Optional
from decimal import Decimal
from django.db.models import QuerySet, Sum, Count
from invoice.models import Invoice
from accounts.models import User
from num2words import num2words
from decimal import Decimal

def get_user_invoices(user: User)->Optional[QuerySet]:
    """
    Simple function to return user invoices
    """
    invoices = Invoice.objects.filter(user=user).order_by('created_at').select_related('customer')
    if invoices:
        return invoices
    return None

def calculate_total_sum_and_count_of_invoices(invoices:Optional[QuerySet])->dict:
    """
    Simple function to calculate sum and count of all invoices
    """
    invoices_total: dict = {}
    if invoices:
        invoices_total = invoices.aggregate(total_price=Sum('total_price'), count=Count('id'))
    return invoices_total

def amount_to_words_lt(amount: Decimal) -> str:
    """
    Convert amount to words
    """
    amount = amount.quantize(Decimal("0.01"))

    euros = int(amount)
    cents = int((amount - euros) * 100)

    euros_words = num2words(euros, lang="lt")

    return (
        f"{euros_words.capitalize()} eur ir {str(cents).zfill(2)} ct"
    )