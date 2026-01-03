from typing import Optional
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from invoice.models import InvoiceItem, Invoice
from invoice.helpers.invoices import recalculate_invoice_total_price_task

@receiver(post_save, sender=InvoiceItem)
def recalculate_invoice_total_price(sender, instance:InvoiceItem, created, **kwargs)->None:
    """
    Simple signal to recalculate invoice total price
    When invoice item is created or updated
    param sender: model class
    param instance: actual instance being saved
    param created: boolean; True if a new record was created
    param kwargs: additional keyword arguments
    return: None
    """
    try:
        invoice:Optional[Invoice] = get_object_or_404(Invoice, invoice_items=instance)        
    except Invoice.DoesNotExist:
        print('Failed to get invoice!')
    if settings.ASYNC:
        recalculate_invoice_total_price_task.delay(invoice.pk)
    else:
        recalculate_invoice_total_price_task(invoice.pk)
    

@receiver(post_delete, sender=InvoiceItem)
def recalculate_invoice_total_price_on_item_delete(sender, instance:InvoiceItem,  **kwargs)->None:
    """
    Simple signal to recalculate invoice total price
    When invoice item is deleted
    param sender: model class
    param instance: actual instance being saved
    param kwargs: additional keyword arguments
    return: None
    """
    invoice_pk = instance.invoice.pk
    try:
        invoice:Optional[Invoice] = get_object_or_404(Invoice, pk=invoice_pk)
    except Invoice.DoesNotExist:
        print('Failed to get invoice!')
        return None
    if settings.ASYNC:
        recalculate_invoice_total_price_task.delay(invoice.pk)
    else:
        recalculate_invoice_total_price_task(invoice.pk)
    