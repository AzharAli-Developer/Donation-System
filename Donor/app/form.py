from django import forms
from  django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from .models import Donor,Volunteer,DonationArea,Donation,Gallery

class LoginForm(AuthenticationForm):
    username=forms.CharField(required=True,label='Username',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    password=forms.CharField(required=True,label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))

class UserForm(UserCreationForm):
    username=forms.CharField(label='Username',widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name=forms.CharField(label='First_Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(label=' Last_Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(label='Email',widget=forms.TextInput(attrs={'class':'form-control'}))
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']

class DonorSignupForm(forms.ModelForm):
    contact=forms.CharField(label='Contact',widget=forms.TextInput(attrs={'class':'form-control'}))
    address=forms.CharField(label='Address',widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model=Donor
        fields=['contact','userpic','address']

class VolunteerSignUpForm(forms.ModelForm):
   contact=forms.IntegerField(label='Contact',widget=forms.TextInput(attrs={'class':'form-control'}))
   address=forms.CharField(label='Address',widget=forms.TextInput(attrs={'class':'form-control'}))
   aboutme=forms.CharField(label='About me',widget=forms.TextInput(attrs={'class':'form-control'}))
   class Meta:
       model = Volunteer
       fields = ['contact', 'userpic', 'idpic', 'address', 'aboutme']

class EditPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs={'class' :'form-control'}))
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class' :'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class' :'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(label='Enter your email',widget=forms.EmailInput(attrs={'class':'form-control'}))

class AgainPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))


class DonationNow(forms.ModelForm):
    class Meta:
        model=Donation
        fields=['donor','donationname','donationpic','collectionAddress','description']

class AdminUpdate(forms.ModelForm):
    class Meta:
        model=Donation
        fields=['status','adminremark']


class VolunteerUpdate(forms.ModelForm):
    class Meta:
        model=Volunteer
        fields=['status','adminremark']


class DonationAreaForm(forms.ModelForm):
    class Meta:
        model=DonationArea
        fields=['areaname','description']

