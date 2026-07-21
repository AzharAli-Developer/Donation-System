"""Forms used by the donation workflow views."""

from __future__ import annotations

from typing import Any

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.models import User

from .models import Donation, DonationArea, DonationStatus, Donor, Volunteer, VolunteerStatus

TEXT_INPUT_CLASS = "form-control"


def text_widget(**attrs: str) -> forms.TextInput:
    attributes = {"class": TEXT_INPUT_CLASS}
    attributes.update(attrs)
    return forms.TextInput(attrs=attributes)


def textarea_widget(**attrs: str) -> forms.Textarea:
    attributes = {"class": TEXT_INPUT_CLASS, "rows": "3"}
    attributes.update(attrs)
    return forms.Textarea(attrs=attributes)


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        label="Username",
        widget=text_widget(placeholder="username"),
    )
    password = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={"class": TEXT_INPUT_CLASS, "placeholder": "password"}),
    )


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=text_widget())
    first_name = forms.CharField(label="First name", widget=text_widget())
    last_name = forms.CharField(label="Last name", widget=text_widget())
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": TEXT_INPUT_CLASS}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": TEXT_INPUT_CLASS}))
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"class": TEXT_INPUT_CLASS}),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class DonorProfileForm(forms.ModelForm):
    contact = forms.CharField(label="Contact", widget=text_widget())
    address = forms.CharField(label="Address", widget=text_widget())

    class Meta:
        model = Donor
        fields = ["contact", "userpic", "address"]


class VolunteerRegistrationForm(forms.ModelForm):
    contact = forms.CharField(label="Contact", widget=text_widget())
    address = forms.CharField(label="Address", widget=text_widget())
    aboutme = forms.CharField(label="About me", widget=text_widget())

    class Meta:
        model = Volunteer
        fields = ["contact", "userpic", "idpic", "address", "aboutme"]


class VolunteerProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="First name", widget=text_widget())
    last_name = forms.CharField(label="Last name", widget=text_widget())
    email = forms.EmailField(label="Email", disabled=True, widget=forms.EmailInput(attrs={"class": TEXT_INPUT_CLASS}))

    class Meta:
        model = Volunteer
        fields = ["contact", "userpic", "idpic", "address", "aboutme"]
        widgets = {
            "contact": text_widget(),
            "address": textarea_widget(),
            "aboutme": textarea_widget(),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user_id:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email

    def save(self, commit: bool = True) -> Volunteer:
        volunteer = super().save(commit=False)
        volunteer.user.first_name = self.cleaned_data["first_name"]
        volunteer.user.last_name = self.cleaned_data["last_name"]
        if commit:
            volunteer.user.save(update_fields=["first_name", "last_name"])
            volunteer.save()
        return volunteer


class StyledPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput(attrs={"class": TEXT_INPUT_CLASS}))
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput(attrs={"class": TEXT_INPUT_CLASS}))
    new_password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"class": TEXT_INPUT_CLASS}),
    )


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Enter your email",
        widget=forms.EmailInput(attrs={"class": TEXT_INPUT_CLASS}),
    )


class AgainPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput(attrs={"class": TEXT_INPUT_CLASS}))
    new_password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"class": TEXT_INPUT_CLASS}),
    )


class DonationCreateForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ["donationname", "donationpic", "collectionAddress", "description"]
        widgets = {
            "donationname": forms.Select(attrs={"class": TEXT_INPUT_CLASS}),
            "collectionAddress": text_widget(),
            "description": text_widget(),
        }


class DonationAdminDecisionForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=[
            (DonationStatus.ACCEPTED, DonationStatus.ACCEPTED.label),
            (DonationStatus.REJECTED, DonationStatus.REJECTED.label),
        ],
        widget=forms.Select(attrs={"class": TEXT_INPUT_CLASS}),
    )

    class Meta:
        model = Donation
        fields = ["status", "adminremark"]
        widgets = {"adminremark": textarea_widget()}


class VolunteerReviewForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=[
            (VolunteerStatus.ACCEPTED, VolunteerStatus.ACCEPTED.label),
            (VolunteerStatus.REJECTED, VolunteerStatus.REJECTED.label),
        ],
        widget=forms.Select(attrs={"class": TEXT_INPUT_CLASS}),
    )

    class Meta:
        model = Volunteer
        fields = ["status", "adminremark"]
        widgets = {"adminremark": textarea_widget()}


class DonationAreaForm(forms.ModelForm):
    class Meta:
        model = DonationArea
        fields = ["areaname", "description"]
        widgets = {
            "areaname": text_widget(),
            "description": textarea_widget(),
        }
