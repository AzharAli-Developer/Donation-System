from django.shortcuts import redirect, render,get_object_or_404
from .models import Donor,Donation,Volunteer,DonationArea
from . form import UserForm,DonorSignupForm,VolunteerSignUpForm,LoginForm,EditPasswordForm,DonationNow,\
    AdminUpdate,VolunteerUpdate,DonationAreaForm
from django .contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, time

# Create your views here.


def index(request):
    return render(request, "index.html")


def gallery(request):
    return render(request, "gallery.html")


def login_admin(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        un=request.POST['username']
        pw=request.POST['password']
        user = authenticate(request, username=un, password=pw)
        if user is not None:
            login(request, user)
            return redirect('index_admin')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login-admin.html', {'error': 'Invalid username or password'})

    else:
        form = LoginForm()
    return render(request, "login-admin.html",{'form':form})


def login_donor(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        un=request.POST['username']
        pw=request.POST['password']
        user = authenticate(request, username=un, password=pw)
        if user is not None:
            login(request, user)
            return redirect('index_donor')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login-donor.html', {'error': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, "login-donor.html",{'form':form})


def login_volunteer(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        un=request.POST['username']
        pw=request.POST['password']
        user = authenticate(request, username=un, password=pw)
        if user is not None:
            login(request, user)
            return redirect('index_volunteer')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, "Invalid Username and Password")
            return render(request, 'login-volunteer.html',)
    else:
        form = LoginForm()
    return render(request, "login-volunteer.html",{'form':form})


def signup_donor(request):
    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = DonorSignupForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            donor = form2.save(commit=False)
            donor.user = user
            donor.save()
            messages.success(request, "Congratulations || Donor profile has been created")

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form1 = UserForm()
        form2 = DonorSignupForm()

    return render(request, "signup_donor.html", {'form1': form1, 'form2': form2})


def signup_volunteer(request):
    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = VolunteerSignUpForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            donor = form2.save(commit=False)
            donor.user = user
            donor.save()
            messages.success(request, "Congratulations || Volunteer profile has been created")

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form1 = UserForm()
        form2 = VolunteerSignUpForm()
    return render(request, "signup_volunteer.html", {'form1': form1, 'form2': form2})


def index_admin(request):
    total_donor = Donor.objects.all().count()
    total_volunteer = Volunteer.objects.all().count()
    total_donation = Donation.objects.all().count()
    new_donation=Donation.objects.all().filter(status='Pending').count()
    accept_donation=Donation.objects.all().filter(status='Accept').count()
    deliever_donation=Donation.objects.all().filter(status='Donation Delivered Successfully').count()
    donation_area=DonationArea.objects.all().count()
    return render(request, "index-admin.html",{'donor':total_donor,'volunteer':total_volunteer,'donation':total_donation,
           'new_donation':new_donation,'accept_donation':accept_donation,'donationarea':donation_area,
            'deliever_donation':deliever_donation })


#  ************************** Admin dashboard ***************************
def all_volunteer(request):
    volunteer=Volunteer.objects.all()
    return render(request, "all-volunteer.html",{'items':volunteer})


def new_volunteer(request):
    volunteer = Volunteer.objects.filter(status='Pending')
    return render(request, "new-volunteer.html",{'volunteer':volunteer})


def accepted_volunteer(request):
    volunteer=Volunteer.objects.filter(status='Accept')
    return render(request, "accepted-volunteer.html",{'volunteer':volunteer})


def rejected_volunteer(request):
    volunteer = Volunteer.objects.filter(status='Reject')
    return render(request, "rejected-volunteer.html",{'volunteer':volunteer})



def accepted_donation(request):
    accept_donations = Donation.objects.filter(status='Accept')
    return render(request, "accepted-donation.html",{'items':accept_donations})

def accepted_donationdetail(request, pid):
    item=Donation.objects.get(id=pid)
    Area=DonationArea.objects.all()
    volunteer=Volunteer.objects.all()
    if request.method == 'POST':
        selected_area_id = request.POST.get('donationarea')
        selected_volunteer_id = request.POST.get('volunteer')

        selected_area = get_object_or_404(DonationArea, id=selected_area_id)
        selected_volunteer = get_object_or_404(Volunteer, id=selected_volunteer_id)
        if item.status == 'Accept':
            item.status = 'Volunteer Allocated'
            item.donationarea = selected_area
            item.volunteer = selected_volunteer
            item.save()
    return render(request, "accepted-donationdetail.html",{'item':item,'areas':Area,'volunteer':volunteer})


def all_donations(request):
    items=Donation.objects.all()
    return render(request, "all-donations.html",{'items':items})


def changepwd_admin(request):
    if request.method == 'POST':
        form = EditPasswordForm(request.user, request.POST)
        if not request.user.is_authenticated:
            return redirect('/login_admin')
        old = request.POST['old_password']
        newpass = request.POST['new_password1']
        confpass = request.POST['new_password2']
        if newpass == confpass:
            user = User.objects.get(id=request.user.id)
            if user.check_password(old):
                user.set_password(newpass)
                user.save()
                messages.success(request, 'Change password successfully')
            else:
                messages.warning(request, "old password are not match")
        else:
            messages.warning(request, "New password and Confirm password both are different")
    else:
        form = EditPasswordForm(request.user)
    return render(request, "changepwd-admin.html",{'form':form})


def donationrec_admin(request):
    return render(request, "donationrec-admin.html")


def donationnotrec_admin(request):
    return render(request, "donationnotrec-admin.html")


def donationdelivered_admin(request):
    items=Donation.objects.filter(status='Donation Delivered Successfully')
    return render(request, "donationdelivered-admin.html",{'items':items})


def add_area(request):
    if request.method == 'POST':
        form=DonationAreaForm(request.POST)
        if form.is_valid():
            form.save()
    form=DonationAreaForm()
    return render(request, "add-area.html",{'form':form})


def edit_area(request, pid):
    Area = DonationArea.objects.get(id=pid)
    if request.method == 'POST':
        form=DonationAreaForm(request.POST,instance=Area)
        if form.is_valid():
            messages.success(request,"Congratulations Update Succesfully")
            form.save()
    form=DonationAreaForm(instance=Area)
    return render(request, "edit-area.html",{'area':Area,'form':form})


def manage_area(request):
    Area=DonationArea.objects.all()
    return render(request, "manage-area.html",{'areas':Area})


def manage_donor(request):
    donor=Donor.objects.all()
    return render(request, "manage-donor.html",{'donor':donor})



def pending_donation(request):
    donor=Donor.objects.get(user=request.user)
    pending_donations = Donation.objects.filter(donor=donor, status='Pending')
    return render(request, "pending-donation.html",{'pending':pending_donations})


def donation_delete(request,pid):
    item = get_object_or_404(Donation, id=pid)
    item.delete()
    return redirect('all_donations')


def new_donation(request):
    new_donation = Donation.objects.all().filter(status='Pending')
    return render(request,'new-donation.html',{'donations':new_donation})



def rejected_donation(request):
    reject_donations = Donation.objects.filter(status='Reject')
    return render(request, "rejected-donation.html",{'items':reject_donations})


def volunteerallocated_donation(request):
    donations = Donation.objects.filter(status='Volunteer Allocated')
    context = {'donations': donations}
    return render(request, "volunteerallocated-donation.html", context)



# **************************** Admin view details ******************************




def view_volunteerdetail(request, pid):
    item=Volunteer.objects.get(id=pid)
    if request.method == 'POST':
        form=VolunteerUpdate(request.POST,instance=item)
        if form.is_valid():
            form.save()
    form=VolunteerUpdate()
    return render(request, "view-volunteerdetail.html",{"item":item,'form':form})


def view_donordetail(request, pid):
    item=Donor.objects.get(pk=pid)
    return render(request, "view-donordetail.html",{'item':item})


def view_donationdetail(request, pid):
    item = Donation.objects.get(pk=pid)
    if request.method=='POST':
        form=AdminUpdate(request.POST,instance=item)
        if form.is_valid():
            form.save()
            item.updationdate=datetime.now()
            item.save()
    else:
        form=AdminUpdate(instance=item)
    return render(request, "view-donationdetail.html",{'item':item,'form':form})




# **************************** donor dashboard ******************************


def index_donor(request):
    donor=Donor.objects.get(user=request.user)
    total=Donation.objects.filter(donor=donor)
    accepted_donations = Donation.objects.filter(donor=donor, status='Accept')
    rejected_donations = Donation.objects.filter(donor=donor, status='Reject')
    pending_donations = Donation.objects.filter(donor=donor, status='Pending')
    total_item=len(total)
    accept=len(accepted_donations)
    reject=len(rejected_donations)
    pending=len(pending_donations)
    return render(request, "index-donor.html",{'item':total_item,'accept':accept,'pending':pending,'reject':reject})


def donate_now(request):
    if request.method =='POST':
        form=DonationNow(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    else:
       form= DonationNow()
    return render(request, "donate-now.html",{'form':form})


def donation_history(request):
    donor=Donor.objects.get(user=request.user)
    form=Donation.objects.filter(donor=donor)
    return render(request, "donation-history.html",{'form':form})


def profile_donor(request):
    item=Donor.objects.get(user=request.user)
    return render(request, "base-db-donor.html",{'item':item})


def changepwd_donor(request):
    if request.method == 'POST':
        form=EditPasswordForm(request.user,request.POST)
        if not request.user.is_authenticated:
            return redirect('/login_donor')
        old=request.POST['old_password']
        newpass=request.POST['new_password1']
        confpass=request.POST['new_password2']
        if  newpass == confpass:
            user= User.objects.get(id=request.user.id)
            if user.check_password(old):
                user.set_password(newpass)
                user.save()
                messages.success(request,'Change password successfully')
            else:
                messages.warning( request ,"old password are not match")
        else:
            messages.warning(request,"new password and confirm password both are different")
    else:
        form=EditPasswordForm(request.user)
    return render(request, "changepwd-donor.html",{'form':form})


def donor_accepted_donation(request):
    donor = Donor.objects.get(user=request.user)
    accept_donations = Donation.objects.filter(donor=donor, status='Accept')
    return render(request, "donor-accepted-donation.html", {'items': accept_donations})


def donor_rejected_donation(request):
    donor = Donor.objects.get(user=request.user)
    reject_donations = Donation.objects.filter(donor=donor, status='Reject')
    return render(request, "donor-rejected-donation.html", {'items': reject_donations})



# **************************  volunteer dashboard  ****************************


def index_volunteer(request):
    volunteer=Volunteer.objects.get(user=request.user)
    donations = Donation.objects.filter(volunteer = volunteer , status = 'Volunteer Allocated').count()
    received_donations = Donation.objects.filter(volunteer = volunteer , status = 'Donation Received').count()
    not_received_donations = Donation.objects.filter(volunteer = volunteer , status = 'Donation Not Received').count()
    delivered=Donation.objects.filter(volunteer = volunteer , status = 'Donation Delivered Successfully').count()
    context={
        'donations':donations,
        'received':received_donations,
        'notreceived':not_received_donations,
        'delivered':delivered
    }
    return render(request, "index-volunteer.html",context)


def collection_req(request):
    volunteer = Volunteer.objects.get(user=request.user)
    donations = Donation.objects.filter(volunteer=volunteer, status='Volunteer Allocated')
    return render(request, "collection-req.html",{'donations':donations})



def donationrec_volunteer(request):
    volunteer = Volunteer.objects.get(user=request.user)
    items = Donation.objects.filter(volunteer=volunteer, status='Donation Received')
    return render(request, "donationrec-volunteer.html",{'items': items})


def donationnotrec_volunteer(request):
    volunteer = Volunteer.objects.get(user=request.user)
    items = Donation.objects.filter(volunteer=volunteer, status='Donation Not Received')
    return render(request, "donationnotrec-volunteer.html",{'items':items})


def donationdelivered_volunteer(request):
    volunteer = Volunteer.objects.get(user=request.user)
    items = Donation.objects.filter(volunteer=volunteer, status='Donation Delivered Successfully')
    return render(request, "donationdelivered-volunteer.html",{'items':items})


def profile_volunteer(request):
    return render(request, "profile-volunteer.html")


def changepwd_volunteer(request):
    if request.method == 'POST':
        form=EditPasswordForm(request.user,request.POST)
        if not request.user.is_authenticated:
            return redirect('/login_donor')
        old=request.POST['old_password']
        newpass=request.POST['new_password1']
        confpass=request.POST['new_password2']
        if  newpass == confpass:
            user= User.objects.get(id=request.user.id)
            if user.check_password(old):
                user.set_password(newpass)
                user.save()
                messages.success(request,'Change password successfully')
            else:
                messages.warning( request ,"old password are not match")
        else:
            messages.warning(request,"new password and confirm password both are different")
    else:
        form=EditPasswordForm(request.user)
    return render(request, "changepwd-volunteer.html",{'form':form})


#******************************** view details  ****************************


def donationdetail_donor(request, pid):
    item=Donation.objects.get(id=pid)
    return render(request, "donationdetail-donor.html",{'item':item})


def donationcollection_detail(request, pid):
    item=Donation.objects.get(id=pid)
    if request.method == "POST":
        volunteer_remark = request.POST.get('volunteerremark')
        status_change=request.POST.get('status')
        if item.status == 'Volunteer Allocated':
            item.status = status_change
            item.volunteerremark = volunteer_remark
            item.save()
    return render(request, "donationcollection-detail.html",{'item':item})


def donationrec_detail(request, pid):
    item=Donation.objects.get(id=pid)
    if request.method == "POST":
        final_feedback = request.POST.get('feedback')
        if item.status == 'Donation Received':
            item.status = final_feedback
            item.save()
    return render(request, "donationrec-detail.html",{'item':item})
