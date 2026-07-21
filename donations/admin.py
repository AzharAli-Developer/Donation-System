"""Django admin configuration for donation workflows."""

from django.contrib import admin

from .models import Donation, DonationArea, Donor, Gallery, Volunteer


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "contact", "address", "regdate")
    list_select_related = ("user",)
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email", "contact")


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "contact", "status", "regdate", "updationdate")
    list_filter = ("status",)
    list_select_related = ("user",)
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email", "contact")


@admin.register(DonationArea)
class DonationAreaAdmin(admin.ModelAdmin):
    list_display = ("id", "areaname", "description", "creationdate")
    search_fields = ("areaname",)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("id", "donor", "donationname", "volunteer", "donationarea", "status", "donationdate")
    list_filter = ("status", "donationname", "donationarea")
    list_select_related = ("donor__user", "volunteer__user", "donationarea")
    search_fields = ("donor__user__username", "volunteer__user__username", "collectionAddress")


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("id", "donation", "deliverypic", "creationdate")
    list_select_related = ("donation",)
