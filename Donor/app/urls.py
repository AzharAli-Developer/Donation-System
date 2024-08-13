from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_view
from .form import MyPasswordResetForm,AgainPasswordForm


urlpatterns = [
    path("", views.index, name="index"),
    path("gallery/", views.gallery, name="gallery"),
    path("login-admin/", views.login_admin, name="login_admin"),
    path("login-donor/", views.login_donor, name="login_donor"),
    path("login-volunteer/", views.login_volunteer, name="login_volunteer"),
    path("signup-donor/", views.signup_donor, name="signup_donor"),
    path("signup-volunteer/", views.signup_volunteer, name="signup_volunteer"),
    path("logout/", auth_view.LogoutView.as_view(next_page='index'), name="logout"),



    # admin dashboard
    path("index-admin/", views.index_admin, name="index_admin"),     #1
    path("pending-donation/", views.pending_donation, name="pending_donation"),     #2
    path("accepted-donation/", views.accepted_donation, name="accepted_donation"),     #3
    path("rejected-donation/", views.rejected_donation, name="rejected_donation"),     #4
    path("volunteerallocated-donation/",views.volunteerallocated_donation,name="volunteerallocated_donation",),     #5
    path("donationrec-admin/", views.donationrec_admin, name="donationrec_admin"),     #6
    path("donationnotrec-admin/", views.donationnotrec_admin, name="donationnotrec_admin"),     #7
    path("donationdelivered-admin/",views.donationdelivered_admin,name="donationdelivered_admin",),     #8
    path("all-donations/", views.all_donations, name="all_donations"),     #9
    path("donation_delete/<int:pid>", views.donation_delete, name="donation_delete"),
    path("new-donation", views.new_donation,name="new_donation"),
    path("manage-donor/", views.manage_donor, name="manage_donor"),     #10
    path("new-volunteer/", views.new_volunteer, name="new_volunteer"),     #11
    path("accepted-volunteer/", views.accepted_volunteer, name="accepted_volunteer"),     #12
    path("rejected-volunteer/", views.rejected_volunteer, name="rejected_volunteer"),     #13
    path("all-volunteer/", views.all_volunteer, name="all_volunteer"),     #14
    path("add-area/", views.add_area, name="add_area"),     #15
    path("edit-area/<int:pid>", views.edit_area, name="edit_area"),     #16
    path("manage-area/", views.manage_area, name="manage_area"),     #17
    path("changepwd-admin/", views.changepwd_admin, name="changepwd_admin"),     #18


    # view details

    path("accepted-donationdetail/<int:pid>",views.accepted_donationdetail,name="accepted_donationdetail",),     #19
    path("view-volunteerdetail/<int:pid>",views.view_volunteerdetail,name="view_volunteerdetail",),     #20
    path("view-donordetail/<int:pid>", views.view_donordetail, name="view_donordetail"),     #21
    path("view-donationdetail/<int:pid>",views.view_donationdetail,name="view_donationdetail",),     #22

    # donar dashboard

    path("index-donor/", views.index_donor, name="index_donor"),
    path("donate-now/", views.donate_now, name="donate_now"),
    path("donation-history/", views.donation_history, name="donation_history"),
    path("profile-donor/", views.profile_donor, name="profile_donor"),
    path("changepwd-donor/", views.changepwd_donor, name="changepwd_donor"),
    path("donor-accepted-donation/", views.donor_accepted_donation, name="donor_accepted_donation"),
    path("donor-rejected-donation/", views.donor_rejected_donation, name="donor_rejected_donation"),

    # volunteer dashboard

    path("index-volunteer/", views.index_volunteer, name="index_volunteer"),     #28
    path("collection-req/", views.collection_req, name="collection_req"),     #29
    path("donationrec-volunteer/",views.donationrec_volunteer,name="donationrec_volunteer",),     #30
    path("donationnotrec-volunteer/",views.donationnotrec_volunteer,name="donationnotrec_volunteer",),     #31
    path("donationdelivered-volunteer/",views.donationdelivered_volunteer,name="donationdelivered_volunteer",),     #32
    path("profile-volunteer/", views.profile_volunteer, name="profile_volunteer"),     #33
    path("changepwd-volunteer/", views.changepwd_volunteer, name="changepwd_volunteer"),     #34

    # vew details

    path("donationdetail-donor/<int:pid>",views.donationdetail_donor,name="donationdetail_donor",),     #35
    path("donationrec-detail/<int:pid>",views.donationrec_detail,name="donationrec_detail",),     #36
    path("donationcollection-detail/<int:pid>",views.donationcollection_detail,name="donationcollection_detail",),    #37



    # password Reset
    path('password_reset', auth_view.PasswordResetView.as_view(template_name='password_reset.html',
                form_class=MyPasswordResetForm),name='password_reset_form'),
    path('password_reset_done',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
                       name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='password_set.html',
                                    form_class=AgainPasswordForm),name='password_reset_confirm'),
    path('password_reset_complete',auth_view.PasswordResetCompleteView.as_view(template_name='password_set_done.html'),
                       name='password_reset_complete'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
