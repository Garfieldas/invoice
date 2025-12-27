from typing import Optional
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from invoice.helpers.invoices import get_user_invoices
from invoice.models import Invoice
from accounts.models import User
from invoice.forms import InvoiceForm, InvoiceItemFormset, InvoiceItemForm

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
    if request.method == "POST":
        form = InvoiceForm(request.POST, user=user)
        formset = InvoiceItemFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            formset.instance = invoice
            formset.save()
            return redirect("invoices")
    else:
        form = InvoiceForm(user=user)
        formset = InvoiceItemFormset()
    
    context["form"] = form
    context["formset"] = formset
    return render(request, "invoices/invoice_form.html", context)