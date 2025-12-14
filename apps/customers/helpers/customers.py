from typing import Optional
from django.db.models import QuerySet
from customers.models import Customer
from accounts.models import User

def get_user_customers(user:Optional[User])->Optional[QuerySet]:
    """
    Function to return users customers
    """
    if not user:
        return None
    return Customer.objects.filter(provider=user)