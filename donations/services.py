"""Business operations for donation and volunteer workflows."""

from __future__ import annotations

import logging

from django.utils import timezone

from .models import Donation, DonationArea, DonationStatus, Donor, Volunteer

logger = logging.getLogger(__name__)


def create_donation(*, donor: Donor, donation: Donation) -> Donation:
    """Attach the authenticated donor to a new donation request."""

    donation.donor = donor
    donation.status = DonationStatus.PENDING
    donation.save()
    logger.info("Donation %s created by donor %s", donation.pk, donor.pk)
    return donation


def review_donation(*, donation: Donation, status: str, admin_remark: str | None = None) -> Donation:
    """Accept or reject a pending donation request."""

    donation.status = status
    donation.adminremark = admin_remark
    donation.updationdate = timezone.now()
    donation.save(update_fields=["status", "adminremark", "updationdate"])
    logger.info("Donation %s reviewed with status %s", donation.pk, status)
    return donation


def allocate_donation(
    *,
    donation: Donation,
    area: DonationArea,
    volunteer: Volunteer,
) -> Donation:
    """Assign an accepted donation to an approved volunteer and distribution area."""

    if donation.status != DonationStatus.ACCEPTED:
        return donation
    donation.status = DonationStatus.VOLUNTEER_ALLOCATED
    donation.donationarea = area
    donation.volunteer = volunteer
    donation.updationdate = timezone.now()
    donation.save(update_fields=["status", "donationarea", "volunteer", "updationdate"])
    logger.info("Donation %s allocated to volunteer %s", donation.pk, volunteer.pk)
    return donation


def record_collection_result(
    *,
    donation: Donation,
    status: str,
    volunteer_remark: str | None = None,
) -> Donation:
    """Record whether an assigned volunteer collected the donation."""

    if donation.status != DonationStatus.VOLUNTEER_ALLOCATED:
        return donation
    donation.status = status
    donation.volunteerremark = volunteer_remark
    donation.updationdate = timezone.now()
    donation.save(update_fields=["status", "volunteerremark", "updationdate"])
    logger.info("Donation %s collection result changed to %s", donation.pk, status)
    return donation


def mark_delivered(*, donation: Donation) -> Donation:
    """Mark a received donation as delivered."""

    if donation.status != DonationStatus.RECEIVED:
        return donation
    donation.status = DonationStatus.DELIVERED
    donation.updationdate = timezone.now()
    donation.save(update_fields=["status", "updationdate"])
    logger.info("Donation %s marked delivered", donation.pk)
    return donation
