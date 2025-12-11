from typing import Optional
from decimal import Decimal
from django.db.models import QuerySet
from invoice.models import Invoice
from accounts.models import User

def get_user_invoices(user: User)->Optional[QuerySet]:
    """
    Simple function to return user invoices
    """
    invoices = Invoice.objects.filter(user=user)
    if invoices:
        return invoices
    return None

def calculate_total_amount_of_invoices(invoices:Optional[QuerySet])->Decimal:
    """
    Simple function to calculate sum of all invoices
    """
    total_price: Decimal = Decimal("0.00")
    if invoices:
        for invoice in invoices:
            total_price += invoice.total_price
    return total_price

def get_invoices_count(invoices:Optional[QuerySet])->Optional[int]:
    """
    Calculate number of user invoices
    """
    if invoices:
        return invoices.count()
    return None

def get_recent_invoices(user: User)->Optional[QuerySet]:
    """
    Ger user recent invoices
    """
    qs = get_user_invoices(user)
    if qs:
        return qs.order_by('created_at').select_related('customer')[:5]
    return None