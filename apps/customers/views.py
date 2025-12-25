from typing import Optional
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from customers.helpers.customers import get_user_customers
from customers.models import Customer
from customers.forms import CustomerForm
from accounts.models import User

@login_required
def customers(request:HttpRequest)->HttpResponse:
    user:Optional[User]  = request.user # type: ignore
    customers: Optional[QuerySet] = get_user_customers(user)
    context: dict = {
        "customers": customers
    }
    return render(request, "customers/customers.html", context)

@login_required
def customer_details(request:HttpRequest, customer_pk:str)->HttpResponse:
    try:
        customer = get_object_or_404(Customer, pk=customer_pk)
    except Customer.DoesNotExist:
        print(f"Failed to get customer {customer_pk}")
    context: dict = {
        "title": "Customer details",
        "description": "Edit customer information or delete the customer.",
        "url": reverse("customers"),
        "update": True,
        "delete_url": reverse('customer_delete', args=[customer.pk])
    }
    if request.method == "POST":
        form: CustomerForm = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer details updated successfully")
    else:
        form = CustomerForm(instance=customer)

    context["form"] = form
    return render(request, 'components/base_form.html', context)

@login_required
def delete_customer(request:HttpRequest, customer_pk:str)->HttpResponse:
    try:
        customer = get_object_or_404(Customer, pk=customer_pk)
    except Customer.DoesNotExist:
        print(f"Failed to get customer {customer_pk}")

    messages.success(request, "Customer deleted successfully")
    customer.delete()
    return redirect('customers')

@login_required
def create_customer(request:HttpRequest)->HttpResponse:
    user = request.user
    context: dict = {
        "title": "Customer creation",
        "description": "All fields are required!",
        "url": reverse("customers")
    }
    if request.method == "POST":
        form = CustomerForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer successfully added!')
            return redirect('customers')
    else:
        form = CustomerForm(user=user)
    context["form"] = form
    return render(request, 'components/base_form.html', context)