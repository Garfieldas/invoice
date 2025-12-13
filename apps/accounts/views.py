from typing import Optional
from decimal import Decimal
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from invoice.helpers.invoices import(
    get_user_invoices,
    calculate_total_sum__and_count_of_invoices
)
from accounts.models import User, SelfInfo
from accounts.forms.self_info_form import SelfInfoForm

@login_required
def dashboard(request:HttpRequest)->HttpResponse:
    user: User = request.user # type: ignore
    invoices:Optional[QuerySet] = get_user_invoices(user)
    invoices_total:dict = {}
    recent_invoices: Optional[QuerySet] = None
    if invoices:
        invoices_total = calculate_total_sum__and_count_of_invoices(invoices)
        recent_invoices = invoices[:5]

    context: dict = {
        "user": user,
        "total_price": invoices_total["total_price"],
        "invoices_count": invoices_total["count"],
        "recent_invoices": recent_invoices
    }

    return render(request, 'dashboard/dashboard.html', context)

@login_required
def self_info(request:HttpRequest)->HttpResponse:
    user: User = request.user # type: ignore
    try:
        self_info: Optional[SelfInfo] = SelfInfo.objects.get(user=user)
    except SelfInfo.DoesNotExist:
        pass
    if request.method == "POST":
        form: SelfInfoForm = SelfInfoForm(request.POST, instance=self_info)
        if form.is_valid():
            form.save()
            messages.success(request, 'Information updated successfully!')
            context: dict = {"form": form}
            return render(request, 'settings/self_info.html', context)
        else:
            context: dict = {"form": form}
            return render(request, 'settings/self_info.html', context)
    form: SelfInfoForm = SelfInfoForm(instance=self_info)
    context: dict = {"form": form}
    return render(request, 'settings/self_info.html', context)

