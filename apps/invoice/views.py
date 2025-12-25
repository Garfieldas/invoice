from typing import Optional
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from invoice.helpers.invoices import get_user_invoices
from accounts.models import User

@login_required
def invoices(request: HttpRequest)->HttpResponse:
    user: User = request.user # type: ignore
    invoices:Optional[QuerySet] = get_user_invoices(user)
    context: dict = {}
    context["invoices"] = invoices
    return render(request, "invoices/invoices.html", context)

