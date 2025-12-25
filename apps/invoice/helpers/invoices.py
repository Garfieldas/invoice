from typing import Optional
from decimal import Decimal
from django.db.models import QuerySet, Sum, Count
from invoice.models import Invoice
from accounts.models import User

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