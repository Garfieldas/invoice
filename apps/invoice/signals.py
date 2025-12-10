from typing import Optional
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.db.models import QuerySet
from django.db.models.signals import post_save, pre_delete
from invoice.models import InvoiceItem, Invoice
from invoice.helpers.invoice_items import (
    get_invoice_items,
    override_invoice_price,
    calculate_invoice_item_price,
    sum_invoice_items_price
)

@receiver(post_save, sender=InvoiceItem)
def recalculate_invoice_total_price(sender, instance:InvoiceItem, created, **kwargs)->None:
    """
    Simple signal to recalculate invoice total price
    If new invoice item created runs logic to check if sum should be added or overriden
    If invoice item updated recalculate total price
    """
    try:
        invoice:Optional[Invoice] = get_object_or_404(Invoice, invoice_items=instance)
        invoice_items:Optional[QuerySet] = get_invoice_items(invoice)
        if created:
            if invoice_items:
                recalculate_price:bool = override_invoice_price(invoice_items)
                if recalculate_price:
                    invoice.total_price = calculate_invoice_item_price(instance)
                else:
                    invoice.total_price += calculate_invoice_item_price(instance)
        else:
            invoice.total_price = sum_invoice_items_price(invoice_items)
        invoice.save()
        
    except Invoice.DoesNotExist:
        print('Failed to get invoice!')

@receiver(pre_delete, sender=InvoiceItem)
def recalculate_invoice_total_price_on_item_delete(sender, instance:InvoiceItem,  **kwargs)->None:
    """
    Simple signal to recalculate invoice total price on item deletion
    """
    try:
        invoice:Optional[Invoice] = get_object_or_404(Invoice, invoice_items=instance)
        invoice_items:Optional[QuerySet] = get_invoice_items(invoice, exclude=instance)
        if invoice_items:
            invoice.total_price = sum_invoice_items_price(invoice_items)
        else:
            invoice.total_price = Decimal("0.00")
        invoice.save()
        
    except Invoice.DoesNotExist:
        print('Failed to get invoice!')
        return None