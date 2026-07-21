"""Regression tests for role access and donation workflow safety."""

from __future__ import annotations

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Donation, DonationStatus, Donor, Volunteer, VolunteerStatus


class DonationSecurityTests(TestCase):
    def setUp(self) -> None:
        self.donor_user = User.objects.create_user(username="donor", password="pass12345")
        self.other_donor_user = User.objects.create_user(username="other-donor", password="pass12345")
        self.admin_user = User.objects.create_superuser(username="admin", password="pass12345")
        self.volunteer_user = User.objects.create_user(username="volunteer", password="pass12345")
        self.other_volunteer_user = User.objects.create_user(username="other-volunteer", password="pass12345")

        self.donor = Donor.objects.create(user=self.donor_user, contact="111", address="Donor address")
        self.other_donor = Donor.objects.create(user=self.other_donor_user, contact="222", address="Other address")
        self.volunteer = Volunteer.objects.create(
            user=self.volunteer_user,
            contact="333",
            address="Volunteer address",
            status=VolunteerStatus.ACCEPTED,
        )
        self.other_volunteer = Volunteer.objects.create(
            user=self.other_volunteer_user,
            contact="444",
            address="Other volunteer address",
            status=VolunteerStatus.ACCEPTED,
        )

    def test_donor_cannot_spoof_donor_id_when_creating_donation(self) -> None:
        self.client.login(username="donor", password="pass12345")

        response = self.client.post(
            reverse("donate_now"),
            {
                "donor": self.other_donor.pk,
                "donationname": "Food Donation",
                "collectionAddress": "Collection address",
                "description": "Food packets",
            },
        )

        self.assertRedirects(response, reverse("donation_history"))
        donation = Donation.objects.get()
        self.assertEqual(donation.donor, self.donor)
        self.assertEqual(donation.status, DonationStatus.PENDING)

    def test_donor_cannot_view_another_donors_donation_detail(self) -> None:
        donation = Donation.objects.create(
            donor=self.other_donor,
            donationname="Books Donation",
            collectionAddress="Other address",
            description="Books",
        )
        self.client.login(username="donor", password="pass12345")

        response = self.client.get(reverse("donationdetail_donor", args=[donation.pk]))

        self.assertEqual(response.status_code, 404)

    def test_volunteer_cannot_view_unassigned_donation_detail(self) -> None:
        donation = Donation.objects.create(
            donor=self.donor,
            volunteer=self.other_volunteer,
            donationname="Cloth Donation",
            collectionAddress="Donor address",
            description="Clothes",
            status=DonationStatus.VOLUNTEER_ALLOCATED,
        )
        self.client.login(username="volunteer", password="pass12345")

        response = self.client.get(reverse("donationcollection_detail", args=[donation.pk]))

        self.assertEqual(response.status_code, 404)

    def test_admin_donation_delete_requires_post(self) -> None:
        donation = Donation.objects.create(
            donor=self.donor,
            donationname="Shoes Donation",
            collectionAddress="Donor address",
            description="Shoes",
        )
        self.client.login(username="admin", password="pass12345")

        get_response = self.client.get(reverse("donation_delete", args=[donation.pk]))
        post_response = self.client.post(reverse("donation_delete", args=[donation.pk]))

        self.assertEqual(get_response.status_code, 405)
        self.assertRedirects(post_response, reverse("all_donations"))
        self.assertFalse(Donation.objects.filter(pk=donation.pk).exists())
