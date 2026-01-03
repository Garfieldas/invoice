from typing import Optional
from decimal import Decimal
from django.db.models import QuerySet, Sum, Count
from invoice.models import Invoice, InvoiceItem
from django_rq import job
from accounts.models import User
from num2words import num2words
from decimal import Decimal

def get_user_invoices(user: User)->Optional[QuerySet]:
    """
    Simple function to return all invoices for given user
    param user: User instance
    return: QuerySet of Invoice instances or None
    """
    invoices = Invoice.objects.filter(user=user).order_by('created_at').select_related('customer')
    if invoices:
        return invoices
    return None

def calculate_total_sum_and_count_of_invoices(invoices:Optional[QuerySet])->dict:
    """
    Simple function to calculate sum and count of all invoices
    param invoices: QuerySet of Invoice instances or None
    return: dict with total price and count of invoices
    """
    invoices_total: dict = {}
    if invoices:
        invoices_total = invoices.aggregate(total_price=Sum('total_price'), count=Count('id'))
    return invoices_total

def get_invoice_items(invoice:Invoice)->Optional[QuerySet]:
    """
    Simple function to return all invoice items for given invoice
    param invoice: Invoice instance
    return: QuerySet of InvoiceItem instances or None
    """
    invoice_items:Optional[QuerySet] = InvoiceItem.objects.filter(invoice=invoice)
    if invoice_items:
        return invoice_items
    return None

def calculate_invoice_items_total_price(invoice_items:Optional[QuerySet])->Decimal:
    """
    Simple function to calculate total price of all invoice items
    param invoice_items: QuerySet of InvoiceItem instances or None
    return: Decimal total price of invoice items"""
    invoice_items_total: Decimal = Decimal("0.0")
    if invoice_items:
        for invoice in invoice_items:
            invoice_items_total += invoice.total_price
    return invoice_items_total

@job('default')
def recalculate_invoice_total_price_task(invoice_pk:str)->None:
    """
    Recalculate invoice total price based on its items
    param invoice_pk: str primary key of Invoice instance
    return: None"""
    try:
        invoice:Optional[Invoice] = Invoice.objects.get(pk=invoice_pk)
    except Invoice.DoesNotExist:
        print(f"Failed to get invoice {invoice_pk}")
    invoice_items:Optional[QuerySet] = get_invoice_items(invoice)
    invoice_items_total_price:Decimal = calculate_invoice_items_total_price(invoice_items)
    if invoice.total_price != invoice_items_total_price:
        invoice.total_price = invoice_items_total_price
        invoice.save(update_fields=["total_price"])
    return None


def amount_to_words_lt(amount: Decimal) -> str:
    """
    Convert a Decimal amount to words in Lithuanian currency format.
    param amount: Decimal amount to convert
    return: str amount in words
    """
    amount = amount.quantize(Decimal("0.01"))

    euros = int(amount)
    cents = int((amount - euros) * 100)

    euros_words = num2words(euros, lang="lt")

    return (
        f"{euros_words.capitalize()} eur ir {str(cents).zfill(2)} ct"
    )