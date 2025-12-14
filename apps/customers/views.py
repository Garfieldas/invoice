from typing import Optional
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from customers.helpers.customers import get_user_customers
from customers.models import Customer
from accounts.models import User

@login_required
def customers(request:HttpRequest)->HttpResponse:
    user:Optional[User]  = request.user # type: ignore
    customers: Optional[QuerySet] = get_user_customers(user)
    context: dict = {
        "customers": customers
    }
    return render(request, "customers/customers.html", context)