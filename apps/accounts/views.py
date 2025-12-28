from typing import Optional
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from invoice.helpers.invoices import(
    get_user_invoices,
    calculate_total_sum_and_count_of_invoices
)
from accounts.models import User, SelfInfo
from accounts.forms.self_info_form import SelfInfoForm
from accounts.forms.auth_forms import LoginForm, CreateUserForm

@login_required
def dashboard(request:HttpRequest)->HttpResponse:
    user: User = request.user # type: ignore
    invoices:Optional[QuerySet] = get_user_invoices(user)
    invoices_total:dict = {"total_price": 0, "count": 0}
    recent_invoices: Optional[QuerySet] = None
    if invoices:
        invoices_total = calculate_total_sum_and_count_of_invoices(invoices)
        recent_invoices = invoices[:5]

    context: dict = {
        "user": user,
        "total_price": invoices_total["total_price"],
        "invoices_count": invoices_total["count"],
        "invoices": recent_invoices
    }

    return render(request, 'dashboard/dashboard.html', context)

@login_required
def self_info(request:HttpRequest)->HttpResponse:
    user: User = request.user # type: ignore
    try:
        self_info: Optional[SelfInfo] = SelfInfo.objects.get(user=user)
    except SelfInfo.DoesNotExist:
        self_info = None
    context: dict = {
        "title": "Profile settings",
        "description": "Additional information for invoice generation",
        "url": reverse("dashboard")
    }
    if not self_info:
        form: SelfInfoForm = SelfInfoForm(request.POST or None)
    else:
        form: SelfInfoForm = SelfInfoForm(request.POST or None, instance=self_info)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            if not self_info:
                instance.user = user
            instance.save()
            messages.success(request, 'Information updated successfully!')
    context["form"] = form
    return render(request, 'components/base_details_page.html', context)

def login_view(request:HttpRequest):
    form: LoginForm = LoginForm(request.POST or None)
    context: dict = {}
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("settings")
    context["form"] = form
    return render(request, "accounts/login_page.html", context)

@login_required
def logout_view(request:HttpRequest)->HttpResponse:
    logout(request)
    return redirect("login")


def register_view(request:HttpRequest):
    form = CreateUserForm(request.POST or None)
    context: dict = {}
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created succesfully")
        return redirect("login")
    context["form"] = form
    return render(request, "accounts/register_page.html", context)
