from functools import wraps
from typing import Callable
from django.shortcuts import redirect

def is_authenticated(view_function:Callable)->Callable:
    """
    simple decorator to redirect authenticated users away from certain views
    param view_function: Callable - the view function to be decorated
    return: Callable - the wrapped view function
    """
    @wraps(view_function)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return view_function(request, *args, **kwargs)
    return _wrapped_view
