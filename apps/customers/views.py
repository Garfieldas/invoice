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
def create_customer(request:HttpRequest)->HttpResponse:
    user = request.user
    context: dict = {
        "title": "Customer creation",
        "description": "All fields are required!",
        "url": reverse("customers")
    }
    form = CustomerForm(request.POST or None, user=user)
    if request.method == "POST":
        if form.is_valid():
            customer = form.save()
            form.save()
            messages.success(request, 'Customer successfully added!')
            return redirect('customer_details', customer_pk=customer.pk)
    context["form"] = form
    return render(request, 'components/base_details_page.html', context)

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
    form: CustomerForm = CustomerForm(request.POST or None, instance=customer)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Customer details updated successfully")
    context["form"] = form
    return render(request, 'components/base_details_page.html', context)

@login_required
def delete_customer(request:HttpRequest, customer_pk:str)->HttpResponse:
    try:
        customer = get_object_or_404(Customer, pk=customer_pk)
    except Customer.DoesNotExist:
        print(f"Failed to get customer {customer_pk}")

    messages.success(request, "Customer deleted successfully")
    customer.delete()
    response:HttpResponse = HttpResponse("", status=200)
    response["HX-Redirect"] = reverse('customers')
    return response