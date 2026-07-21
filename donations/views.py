"""HTTP views for the Donation and Volunteer Management System."""

from __future__ import annotations

import logging
from typing import Any, cast

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .decorators import admin_required, donor_required, volunteer_required
from .forms import (
    DonationAdminDecisionForm,
    DonationAreaForm,
    DonationCreateForm,
    DonorProfileForm,
    LoginForm,
    StyledPasswordChangeForm,
    UserRegistrationForm,
    VolunteerProfileForm,
    VolunteerRegistrationForm,
    VolunteerReviewForm,
)
from .models import Donation, DonationArea, DonationStatus, Donor, Volunteer, VolunteerStatus
from .selectors import (
    admin_dashboard_counts,
    approved_volunteers,
    delivered_gallery_items,
    donation_areas,
    donation_queryset,
    donations_by_status,
    donations_for_donor,
    donations_for_volunteer,
    donor_dashboard_counts,
    donor_queryset,
    volunteer_dashboard_counts,
    volunteer_queryset,
)
from .services import allocate_donation, create_donation, mark_delivered, record_collection_result, review_donation

logger = logging.getLogger(__name__)


def _authenticated_donor(request: HttpRequest) -> Donor:
    return cast(Donor, cast(Any, request.user).donor)


def _authenticated_volunteer(request: HttpRequest) -> Volunteer:
    return cast(Volunteer, cast(Any, request.user).volunteer)


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


def gallery(request: HttpRequest) -> HttpResponse:
    return render(request, "gallery.html", {"gallery_items": delivered_gallery_items()})


def _role_login(
    request: HttpRequest,
    *,
    template_name: str,
    role_name: str,
    redirect_name: str,
) -> HttpResponse:
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        role_error = _login_role_error(user, role_name)
        if role_error:
            messages.error(request, role_error)
        else:
            login(request, user)
            logger.info("%s user %s logged in", role_name, user.pk)
            return redirect(redirect_name)
    elif request.method == "POST":
        messages.error(request, "Invalid username or password.")
    return render(request, template_name, {"form": form})


def _login_role_error(user: User, role_name: str) -> str | None:
    if role_name == "admin" and not (user.is_staff or user.is_superuser):
        return "Please use an administrator account."
    if role_name == "donor" and not hasattr(user, "donor"):
        return "Please use a donor account."
    if role_name == "volunteer":
        volunteer = getattr(user, "volunteer", None)
        if volunteer is None:
            return "Please use a volunteer account."
        if volunteer.status != VolunteerStatus.ACCEPTED:
            return "Your volunteer account is waiting for admin approval."
    return None


def login_admin(request: HttpRequest) -> HttpResponse:
    return _role_login(request, template_name="login-admin.html", role_name="admin", redirect_name="index_admin")


def login_donor(request: HttpRequest) -> HttpResponse:
    return _role_login(request, template_name="login-donor.html", role_name="donor", redirect_name="index_donor")


def login_volunteer(request: HttpRequest) -> HttpResponse:
    return _role_login(
        request,
        template_name="login-volunteer.html",
        role_name="volunteer",
        redirect_name="index_volunteer",
    )


def signup_donor(request: HttpRequest) -> HttpResponse:
    user_form = UserRegistrationForm(request.POST or None)
    donor_form = DonorProfileForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and user_form.is_valid() and donor_form.is_valid():
        with transaction.atomic():
            user = user_form.save()
            donor = donor_form.save(commit=False)
            donor.user = user
            donor.save()
        messages.success(request, "Donor profile has been created. You can now sign in.")
        return redirect("login_donor")

    if request.method == "POST":
        messages.error(request, "Please correct the errors below.")
    return render(request, "signup_donor.html", {"form1": user_form, "form2": donor_form})


def signup_volunteer(request: HttpRequest) -> HttpResponse:
    user_form = UserRegistrationForm(request.POST or None)
    volunteer_form = VolunteerRegistrationForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and user_form.is_valid() and volunteer_form.is_valid():
        with transaction.atomic():
            user = user_form.save()
            volunteer = volunteer_form.save(commit=False)
            volunteer.user = user
            volunteer.save()
        messages.success(request, "Volunteer profile has been created and is waiting for admin approval.")
        return redirect("login_volunteer")

    if request.method == "POST":
        messages.error(request, "Please correct the errors below.")
    return render(request, "signup_volunteer.html", {"form1": user_form, "form2": volunteer_form})


@admin_required
def index_admin(request: HttpRequest) -> HttpResponse:
    return render(request, "index-admin.html", admin_dashboard_counts())


@admin_required
def all_volunteer(request: HttpRequest) -> HttpResponse:
    return render(request, "all-volunteer.html", {"items": volunteer_queryset()})


@admin_required
def new_volunteer(request: HttpRequest) -> HttpResponse:
    return render(request, "new-volunteer.html", {"volunteer": volunteer_queryset(VolunteerStatus.PENDING)})


@admin_required
def accepted_volunteer(request: HttpRequest) -> HttpResponse:
    return render(request, "accepted-volunteer.html", {"volunteer": volunteer_queryset(VolunteerStatus.ACCEPTED)})


@admin_required
def rejected_volunteer(request: HttpRequest) -> HttpResponse:
    return render(request, "rejected-volunteer.html", {"volunteer": volunteer_queryset(VolunteerStatus.REJECTED)})


@admin_required
def accepted_donation(request: HttpRequest) -> HttpResponse:
    return render(request, "accepted-donation.html", {"items": donations_by_status(DonationStatus.ACCEPTED)})


@admin_required
def accepted_donationdetail(request: HttpRequest, pid: int) -> HttpResponse:
    donation = get_object_or_404(donation_queryset(), id=pid)

    if request.method == "POST":
        area = get_object_or_404(DonationArea, id=request.POST.get("donationarea"))
        volunteer = get_object_or_404(approved_volunteers(), id=request.POST.get("volunteer"))
        allocate_donation(donation=donation, area=area, volunteer=volunteer)
        messages.success(request, "Donation allocated successfully.")
        return redirect("accepted_donationdetail", pid=donation.pk)

    context = {
        "item": donation,
        "areas": donation_areas(),
        "volunteer": approved_volunteers(),
    }
    return render(request, "accepted-donationdetail.html", context)


@admin_required
def all_donations(request: HttpRequest) -> HttpResponse:
    return render(request, "all-donations.html", {"items": donation_queryset()})


@admin_required
def changepwd_admin(request: HttpRequest) -> HttpResponse:
    return _change_password(request, "changepwd-admin.html")


@admin_required
def donationrec_admin(request: HttpRequest) -> HttpResponse:
    return render(request, "donationrec-admin.html", {"items": donations_by_status(DonationStatus.RECEIVED)})


@admin_required
def donationnotrec_admin(request: HttpRequest) -> HttpResponse:
    return render(request, "donationnotrec-admin.html", {"items": donations_by_status(DonationStatus.NOT_RECEIVED)})


@admin_required
def donationdelivered_admin(request: HttpRequest) -> HttpResponse:
    return render(request, "donationdelivered-admin.html", {"items": donations_by_status(DonationStatus.DELIVERED)})


@admin_required
def add_area(request: HttpRequest) -> HttpResponse:
    form = DonationAreaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Donation area created successfully.")
        return redirect("manage_area")
    return render(request, "add-area.html", {"form": form})


@admin_required
def edit_area(request: HttpRequest, pid: int) -> HttpResponse:
    area = get_object_or_404(DonationArea, id=pid)
    form = DonationAreaForm(request.POST or None, instance=area)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Donation area updated successfully.")
        return redirect("manage_area")
    return render(request, "edit-area.html", {"area": area, "form": form})


@admin_required
def manage_area(request: HttpRequest) -> HttpResponse:
    return render(request, "manage-area.html", {"areas": donation_areas()})


@admin_required
def manage_donor(request: HttpRequest) -> HttpResponse:
    return render(request, "manage-donor.html", {"donor": donor_queryset()})


@donor_required
def pending_donation(request: HttpRequest) -> HttpResponse:
    pending = donations_for_donor(_authenticated_donor(request), DonationStatus.PENDING)
    return render(request, "pending-donation.html", {"pending": pending})


@admin_required
@require_POST
def donation_delete(request: HttpRequest, pid: int) -> HttpResponse:
    donation = get_object_or_404(Donation, id=pid)
    donation.delete()
    messages.success(request, "Donation deleted successfully.")
    return redirect("all_donations")


@admin_required
def new_donation(request: HttpRequest) -> HttpResponse:
    return render(request, "new-donation.html", {"donations": donations_by_status(DonationStatus.PENDING)})


@admin_required
def rejected_donation(request: HttpRequest) -> HttpResponse:
    return render(request, "rejected-donation.html", {"items": donations_by_status(DonationStatus.REJECTED)})


@admin_required
def volunteerallocated_donation(request: HttpRequest) -> HttpResponse:
    donations = donations_by_status(DonationStatus.VOLUNTEER_ALLOCATED)
    return render(request, "volunteerallocated-donation.html", {"donations": donations})


@admin_required
def view_volunteerdetail(request: HttpRequest, pid: int) -> HttpResponse:
    volunteer = get_object_or_404(volunteer_queryset(), id=pid)
    form = VolunteerReviewForm(request.POST or None, instance=volunteer)

    if request.method == "POST" and form.is_valid():
        volunteer = form.save(commit=False)
        volunteer.updationdate = timezone.now()
        volunteer.save(update_fields=["status", "adminremark", "updationdate"])
        messages.success(request, "Volunteer review updated successfully.")
        return redirect("view_volunteerdetail", pid=volunteer.pk)

    return render(request, "view-volunteerdetail.html", {"item": volunteer, "form": form})


@admin_required
def view_donordetail(request: HttpRequest, pid: int) -> HttpResponse:
    donor = get_object_or_404(donor_queryset(), pk=pid)
    return render(request, "view-donordetail.html", {"item": donor})


@admin_required
def view_donationdetail(request: HttpRequest, pid: int) -> HttpResponse:
    donation = get_object_or_404(donation_queryset(), pk=pid)
    form = DonationAdminDecisionForm(request.POST or None, instance=donation)

    if request.method == "POST" and form.is_valid() and donation.status == DonationStatus.PENDING:
        review_donation(
            donation=donation,
            status=form.cleaned_data["status"],
            admin_remark=form.cleaned_data["adminremark"],
        )
        messages.success(request, "Donation request updated successfully.")
        return redirect("view_donationdetail", pid=donation.pk)

    return render(request, "view-donationdetail.html", {"item": donation, "form": form})


@donor_required
def index_donor(request: HttpRequest) -> HttpResponse:
    return render(request, "index-donor.html", donor_dashboard_counts(_authenticated_donor(request)))


@donor_required
def donate_now(request: HttpRequest) -> HttpResponse:
    form = DonationCreateForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        donation = form.save(commit=False)
        create_donation(donor=_authenticated_donor(request), donation=donation)
        messages.success(request, "Donation request submitted successfully.")
        return redirect("donation_history")
    return render(request, "donate-now.html", {"form": form})


@donor_required
def donation_history(request: HttpRequest) -> HttpResponse:
    return render(request, "donation-history.html", {"form": donations_for_donor(_authenticated_donor(request))})


@donor_required
def profile_donor(request: HttpRequest) -> HttpResponse:
    return render(request, "profile-donor.html", {"item": _authenticated_donor(request)})


@donor_required
def changepwd_donor(request: HttpRequest) -> HttpResponse:
    return _change_password(request, "changepwd-donor.html")


@donor_required
def donor_accepted_donation(request: HttpRequest) -> HttpResponse:
    donations = donations_for_donor(_authenticated_donor(request), DonationStatus.ACCEPTED)
    return render(request, "donor-accepted-donation.html", {"items": donations})


@donor_required
def donor_rejected_donation(request: HttpRequest) -> HttpResponse:
    donations = donations_for_donor(_authenticated_donor(request), DonationStatus.REJECTED)
    return render(request, "donor-rejected-donation.html", {"items": donations})


@volunteer_required
def index_volunteer(request: HttpRequest) -> HttpResponse:
    return render(request, "index-volunteer.html", volunteer_dashboard_counts(_authenticated_volunteer(request)))


@volunteer_required
def collection_req(request: HttpRequest) -> HttpResponse:
    donations = donations_for_volunteer(_authenticated_volunteer(request), DonationStatus.VOLUNTEER_ALLOCATED)
    return render(request, "collection-req.html", {"donations": donations})


@volunteer_required
def donationrec_volunteer(request: HttpRequest) -> HttpResponse:
    donations = donations_for_volunteer(_authenticated_volunteer(request), DonationStatus.RECEIVED)
    return render(request, "donationrec-volunteer.html", {"items": donations})


@volunteer_required
def donationnotrec_volunteer(request: HttpRequest) -> HttpResponse:
    donations = donations_for_volunteer(_authenticated_volunteer(request), DonationStatus.NOT_RECEIVED)
    return render(request, "donationnotrec-volunteer.html", {"items": donations})


@volunteer_required
def donationdelivered_volunteer(request: HttpRequest) -> HttpResponse:
    donations = donations_for_volunteer(_authenticated_volunteer(request), DonationStatus.DELIVERED)
    return render(request, "donationdelivered-volunteer.html", {"items": donations})


@volunteer_required
def profile_volunteer(request: HttpRequest) -> HttpResponse:
    volunteer = _authenticated_volunteer(request)
    form = VolunteerProfileForm(request.POST or None, request.FILES or None, instance=volunteer)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("profile_volunteer")
    return render(request, "profile-volunteer.html", {"volunteer": volunteer, "form": form})


@volunteer_required
def changepwd_volunteer(request: HttpRequest) -> HttpResponse:
    return _change_password(request, "changepwd-volunteer.html")


@donor_required
def donationdetail_donor(request: HttpRequest, pid: int) -> HttpResponse:
    donation = get_object_or_404(donations_for_donor(_authenticated_donor(request)), id=pid)
    return render(request, "donationdetail-donor.html", {"item": donation})


@volunteer_required
def donationcollection_detail(request: HttpRequest, pid: int) -> HttpResponse:
    donation = get_object_or_404(donations_for_volunteer(_authenticated_volunteer(request)), id=pid)
    if request.method == "POST":
        status = request.POST.get("status")
        if status in {DonationStatus.RECEIVED, DonationStatus.NOT_RECEIVED}:
            record_collection_result(
                donation=donation,
                status=status,
                volunteer_remark=request.POST.get("volunteerremark"),
            )
            messages.success(request, "Collection status updated successfully.")
            return redirect("donationcollection_detail", pid=donation.pk)
        messages.error(request, "Please select a valid collection status.")
    return render(request, "donationcollection-detail.html", {"item": donation})


@volunteer_required
def donationrec_detail(request: HttpRequest, pid: int) -> HttpResponse:
    donation = get_object_or_404(donations_for_volunteer(_authenticated_volunteer(request)), id=pid)
    if request.method == "POST":
        if request.POST.get("feedback") == DonationStatus.DELIVERED:
            mark_delivered(donation=donation)
            messages.success(request, "Donation marked as delivered.")
            return redirect("donationrec_detail", pid=donation.pk)
        messages.error(request, "Please select a valid delivery status.")
    return render(request, "donationrec-detail.html", {"item": donation})


def _change_password(request: HttpRequest, template_name: str) -> HttpResponse:
    form = StyledPasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Password changed successfully.")
        resolver_match = request.resolver_match
        return redirect(resolver_match.url_name if resolver_match and resolver_match.url_name else "index")
    return render(request, template_name, {"form": form})
