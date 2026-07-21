"""Read-only query helpers for donation workflows."""

from __future__ import annotations

from django.db.models import Count, Q, QuerySet

from .models import Donation, DonationArea, DonationStatus, Donor, Gallery, Volunteer, VolunteerStatus


def donation_queryset() -> QuerySet[Donation]:
    """Return donations with common relationships eagerly loaded."""

    return Donation.objects.select_related("donor__user", "volunteer__user", "donationarea")


def donations_by_status(status: str) -> QuerySet[Donation]:
    return donation_queryset().filter(status=status)


def donations_for_donor(donor: Donor, status: str | None = None) -> QuerySet[Donation]:
    queryset = donation_queryset().filter(donor=donor)
    if status:
        queryset = queryset.filter(status=status)
    return queryset


def donations_for_volunteer(volunteer: Volunteer, status: str | None = None) -> QuerySet[Donation]:
    queryset = donation_queryset().filter(volunteer=volunteer)
    if status:
        queryset = queryset.filter(status=status)
    return queryset


def approved_volunteers() -> QuerySet[Volunteer]:
    return Volunteer.objects.select_related("user").filter(status=VolunteerStatus.ACCEPTED)


def volunteer_queryset(status: str | None = None) -> QuerySet[Volunteer]:
    queryset = Volunteer.objects.select_related("user")
    if status:
        queryset = queryset.filter(status=status)
    return queryset


def donor_queryset() -> QuerySet[Donor]:
    return Donor.objects.select_related("user")


def donation_areas() -> QuerySet[DonationArea]:
    return DonationArea.objects.all()


def delivered_gallery_items() -> QuerySet[Gallery]:
    return Gallery.objects.select_related(
        "donation__donor__user",
        "donation__volunteer__user",
        "donation__donationarea",
    ).filter(
        donation__status=DonationStatus.DELIVERED,
    )


def admin_dashboard_counts() -> dict[str, int]:
    donation_counts = Donation.objects.aggregate(
        total=Count("id"),
        pending=Count("id", filter=Q(status=DonationStatus.PENDING)),
        accepted=Count("id", filter=Q(status=DonationStatus.ACCEPTED)),
        delivered=Count("id", filter=Q(status=DonationStatus.DELIVERED)),
    )
    return {
        "donor": Donor.objects.count(),
        "volunteer": Volunteer.objects.count(),
        "donation": donation_counts["total"] or 0,
        "new_donation": donation_counts["pending"] or 0,
        "accept_donation": donation_counts["accepted"] or 0,
        "deliever_donation": donation_counts["delivered"] or 0,
        "donationarea": DonationArea.objects.count(),
    }


def donor_dashboard_counts(donor: Donor) -> dict[str, int]:
    counts = Donation.objects.filter(donor=donor).aggregate(
        total=Count("id"),
        accepted=Count("id", filter=Q(status=DonationStatus.ACCEPTED)),
        rejected=Count("id", filter=Q(status=DonationStatus.REJECTED)),
        pending=Count("id", filter=Q(status=DonationStatus.PENDING)),
    )
    return {
        "item": counts["total"] or 0,
        "accept": counts["accepted"] or 0,
        "reject": counts["rejected"] or 0,
        "pending": counts["pending"] or 0,
    }


def volunteer_dashboard_counts(volunteer: Volunteer) -> dict[str, int]:
    counts = Donation.objects.filter(volunteer=volunteer).aggregate(
        allocated=Count("id", filter=Q(status=DonationStatus.VOLUNTEER_ALLOCATED)),
        received=Count("id", filter=Q(status=DonationStatus.RECEIVED)),
        not_received=Count("id", filter=Q(status=DonationStatus.NOT_RECEIVED)),
        delivered=Count("id", filter=Q(status=DonationStatus.DELIVERED)),
    )
    return {
        "donations": counts["allocated"] or 0,
        "received": counts["received"] or 0,
        "notreceived": counts["not_received"] or 0,
        "delivered": counts["delivered"] or 0,
    }
