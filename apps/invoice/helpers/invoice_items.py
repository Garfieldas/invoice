from typing import Optional
from decimal import Decimal
from django.db.models import QuerySet
from invoice.models import Invoice, InvoiceItem

def get_invoice_items(invoice: Invoice, exclude:Optional[InvoiceItem]=None)->Optional[QuerySet]:
    """
    Get invoice items for current invoice. Optionaly exclude invoice item
    """
    invoice_items:QuerySet[InvoiceItem] = InvoiceItem.objects.filter(invoice=invoice)
    if not invoice_items:
        return None
    if exclude:
        return invoice_items.exclude(pk=exclude.pk)
    else:
        return invoice_items

def override_invoice_price(invoice_items:Optional[QuerySet])->bool:
    """
    Determine if invoice previosly had any invoice items
    param invoice_items: QuerySet of invoice items
    return: True if no invoice items exist, False otherwise
    """
    if not invoice_items:
        return True
    return False

def calculate_invoice_item_price(invoice_item:InvoiceItem)->Decimal:
    """
    Calculate invoice item total price based on amout and single unit price
    param invoice_item: InvoiceItem instance
    return: Total price as Decimal
    """
    return invoice_item.amount * invoice_item.price

def sum_invoice_items_price(invoice_items:Optional[QuerySet])->Optional[Decimal]:
    """
    Sum price of all invoice items
    param invoice_items: QuerySet of invoice items
    return: Total price as Decimal or None if no items exist
    """
    if not invoice_items:
        return None
    total_price:Decimal = Decimal("0.00")
    for item in invoice_items:
        total_price += calculate_invoice_item_price(item)
    return total_price

