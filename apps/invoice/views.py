from typing import Optional
from weasyprint import HTML
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models import QuerySet
from accounts.models import User, SelfInfo
from invoice.helpers.invoices import get_user_invoices, get_invoice_items, amount_to_words_lt
from invoice.helpers.pdf import generate_invoice_pdf
from invoice.models import Invoice
from invoice.forms import InvoiceForm, InvoiceItemFormset

@login_required
def invoices(request: HttpRequest)->HttpResponse:
    user: User = request.user # type: ignore
    invoices:Optional[QuerySet] = get_user_invoices(user)
    context: dict = {}
    context["invoices"] = invoices
    return render(request, "invoices/invoices.html", context)

@login_required
def create_invoice(request: HttpRequest) -> HttpResponse:
    user = request.user # type: ignore
    context: dict = {
        "title": "Invoice creation",
        "description": "All fields are required!",
        "url": reverse("invoices")
    }
    form = InvoiceForm(request.POST or None, user=user)
    formset = InvoiceItemFormset(request.POST or None)
    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            formset.instance = invoice
            formset.save()
            messages.success(request, "Invoice created successfully")
            return redirect("invoice-details", invoice_pk=invoice.pk)
    context["form"] = form
    context["formset"] = formset
    return render(request, "invoices/invoice_details.html", context)

@login_required
def invoice_details(request:HttpRequest, invoice_pk: str)->HttpResponse:
    try:
        invoice:Optional[Invoice] = Invoice.objects.get(pk=invoice_pk)
    except Invoice.DoesNotExist:
        pass
    context: dict = {
        "title": "Invoice details",
        "description": "details page",
        "url": reverse("invoices"),
        "update": True,
        "delete_url": reverse('invoice_delete', args=[invoice.pk])
    }
    user = request.user
    form = InvoiceForm(request.POST or None, instance=invoice, user=user)
    formset = InvoiceItemFormset(request.POST or None, instance=invoice)
    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Invoice details updated successfully")
            return redirect('invoice-details', invoice_pk=invoice.pk)
        else:
            messages.error(request, 'At least one invoice item is required')
    context["form"] = form
    context["formset"] = formset
    return render(request, "invoices/invoice_details.html", context)

@login_required
def delete_invoice(request:HttpRequest, invoice_pk:str)->HttpResponse:
    try:
        invoice:Optional[Invoice] = Invoice.objects.get(pk=invoice_pk)
    except Invoice.DoesNotExist:
        pass
    invoice.delete()
    response:HttpResponse = HttpResponse("", status=200)
    response["HX-Redirect"] = reverse('invoices')
    return response

@login_required
def create_invoice_pdf(request:HttpRequest, invoice_pk:str):
    try:
        user: User = request.user # type: ignore
        invoice:Invoice = Invoice.objects.select_related('customer').get(pk=invoice_pk)
        invoice_items:Optional[QuerySet] = get_invoice_items(invoice)
        self_info:SelfInfo = SelfInfo.objects.get(user=user)
        customer = invoice.customer
    except Exception as e:
        print(e)
        pass
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
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="invoice-{invoice.invoice_number}.pdf"'
    return response


def debug_invoice(request: HttpRequest)->HttpResponse:
    invoice_pk = 2
    pdf = generate_invoice_pdf(2)
    return HttpResponse('Test')