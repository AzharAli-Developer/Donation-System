"""Access-control decorators for role-specific views."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from .models import VolunteerStatus

ViewFunc = Callable[..., HttpResponse]


def admin_required(view_func: ViewFunc) -> ViewFunc:
    @login_required(login_url="login_admin")
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_staff or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, "You do not have permission to access the admin area.")
        return redirect("login_admin")

    return wrapper


def donor_required(view_func: ViewFunc) -> ViewFunc:
    @login_required(login_url="login_donor")
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if hasattr(request.user, "donor"):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Please sign in with a donor account.")
        return redirect("login_donor")

    return wrapper


def volunteer_required(view_func: ViewFunc) -> ViewFunc:
    @login_required(login_url="login_volunteer")
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        volunteer = getattr(request.user, "volunteer", None)
        if volunteer and volunteer.status == VolunteerStatus.ACCEPTED:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Your volunteer account must be approved before accessing this page.")
        return redirect("login_volunteer")

    return wrapper
