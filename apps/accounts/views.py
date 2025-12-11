from typing import Optional
from decimal import Decimal
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.contrib.auth.decorators import login_required
from invoice.helpers.invoices import get_user_invoices, get_recent_invoices, get_invoices_count, calculate_total_amount_of_invoices
from accounts.models import User

@login_required
def dashboard(request:HttpRequest)->HttpResponse:
    user: User = request.user
    invoices:Optional[QuerySet] = get_user_invoices(user)
    if invoices:
        total_price:Decimal = calculate_total_amount_of_invoices(invoices)
        invoices_count:Optional[int] = get_invoices_count(invoices)
        recent_invoices:Optional[QuerySet] = get_recent_invoices(user)

    context: dict = {
        "user": user,
        "total_price": total_price,
        "invoices_count": invoices_count,
        "recent_invoices": recent_invoices
    }

    return render(request, 'dashboard/dashboard.html', context)
