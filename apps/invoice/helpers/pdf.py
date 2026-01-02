from typing import Optional
from weasyprint import HTML
from django.db.models import QuerySet
from django.template.loader import render_to_string
from invoice.models import Invoice
from django_rq import job
from customers.models import Customer
from invoice.helpers.invoices import (
    get_invoice_items,
    amount_to_words_lt
)
from accounts.models import User, SelfInfo

@job('low')
def generate_invoice_pdf(invoice_pk:str):
    try:
        invoice: Invoice = Invoice.objects.select_related('customer', 'user').get(pk=invoice_pk)
        user: User = invoice.user
        self_info: SelfInfo = SelfInfo.objects.get(user=user)
        invoice_items:Optional[QuerySet] = get_invoice_items(invoice)
        customer: Customer = invoice.customer
    except Exception as e:
        print(f"failed to get invoice data  error: {e}")
    amount_words = amount_to_words_lt(invoice.total_price)
    context: dict = {
        "user": user,
        "invoice": invoice,
        "customer": customer,
        "self_info": self_info,
        "invoice_items": invoice_items,
        "amount_words": amount_words
    }
    html_to_string = render_to_string("components/invoice_to_pdf.html", context)
    pdf = HTML(string=html_to_string).write_pdf()
    return pdf