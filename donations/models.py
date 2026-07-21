"""Database models for donor, volunteer, and donation workflows."""

from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models


class VolunteerStatus(models.TextChoices):
    """Review states for volunteer registrations."""

    PENDING = "Pending", "Pending"
    ACCEPTED = "Accept", "Accept"
    REJECTED = "Reject", "Reject"


class DonationType(models.TextChoices):
    """Supported donation categories."""

    FOOD = "Food Donation", "Food Donation"
    CLOTHES = "Cloth Donation", "Cloth Donation"
    SHOES = "Shoes Donation", "Shoes Donation"
    BOOKS = "Books Donation", "Books Donation"
    FURNITURE = "Furniture Donation", "Furniture Donation"
    HOME = "Home Donate", "Home Donate"
    APPLIANCE = "Frig Donation", "Fridge Donation"
    BICYCLE = "Byc Donation", "Bicycle Donation"
    OTHER = "Others", "Others"


class DonationStatus(models.TextChoices):
    """Workflow states for a donation request."""

    PENDING = "Pending", "Pending"
    ACCEPTED = "Accept", "Accept"
    REJECTED = "Reject", "Reject"
    VOLUNTEER_ALLOCATED = "Volunteer Allocated", "Volunteer Allocated"
    VOLUNTEER_NOT_ALLOCATED = "Volunteer Not Allocated", "Volunteer Not Allocated"
    RECEIVED = "Donation Received", "Donation Received"
    NOT_RECEIVED = "Donation Not Received", "Donation Not Received"
    DELIVERED = "Donation Delivered Successfully", "Donation Delivered Successfully"


class Donor(models.Model):
    """Profile data for a user who creates donation requests."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="donor")
    contact = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    userpic = models.ImageField(upload_to="myimg", null=True, blank=True)
    regdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-regdate"]

    def __str__(self) -> str:
        return self.user.get_full_name() or self.user.username


class Volunteer(models.Model):
    """Profile and approval data for users who collect donations."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="volunteer")
    contact = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    userpic = models.ImageField(upload_to="volunteer", null=True, blank=True)
    idpic = models.ImageField(upload_to="volunteer", null=True, blank=True)
    aboutme = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(
        choices=VolunteerStatus.choices,
        default=VolunteerStatus.PENDING,
        max_length=20,
    )
    regdate = models.DateTimeField(auto_now_add=True)
    adminremark = models.CharField(max_length=300, null=True, blank=True)
    updationdate = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-regdate"]

    def __str__(self) -> str:
        return self.user.get_full_name() or self.user.username


class DonationArea(models.Model):
    """Distribution area where collected donations can be delivered."""

    areaname = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    creationdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["areaname"]

    def __str__(self) -> str:
        return self.areaname


class Donation(models.Model):
    """A donation request submitted by a donor and processed by staff."""

    donor = models.ForeignKey(
        Donor,
        on_delete=models.CASCADE,
        null=True,
        related_name="donations",
    )
    donationname = models.CharField(
        choices=DonationType.choices,
        max_length=20,
        null=True,
    )
    donationpic = models.ImageField(upload_to="donation", null=True, blank=True)
    collectionAddress = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=120, null=True, blank=True)
    status = models.CharField(
        choices=DonationStatus.choices,
        default=DonationStatus.PENDING,
        max_length=50,
        db_index=True,
    )
    donationdate = models.DateTimeField(null=True, auto_now_add=True)
    adminremark = models.CharField(max_length=128, null=True, blank=True)
    volunteer = models.ForeignKey(
        Volunteer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_donations",
    )
    donationarea = models.ForeignKey(
        DonationArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="donations",
    )
    volunteerremark = models.CharField(max_length=128, null=True, blank=True)
    updationdate = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-donationdate"]
        indexes = [
            models.Index(fields=["status", "donationdate"]),
            models.Index(fields=["donor", "status"]),
            models.Index(fields=["volunteer", "status"]),
        ]

    def __str__(self) -> str:
        return f"{self.donationname or 'Donation'} #{self.pk}"


class Gallery(models.Model):
    """Public gallery image connected to a delivered donation."""

    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name="gallery_items")
    deliverypic = models.FileField(upload_to="gallery", null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creationdate"]
        verbose_name_plural = "Gallery items"

    def __str__(self) -> str:
        return f"Gallery item #{self.pk}"


# Backward-compatible names used by older templates or imports.
DONATION_CHOICES = DonationType.choices
DONATION_STATUS = DonationStatus.choices
