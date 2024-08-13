from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact=models.IntegerField(null=True)
    address=models.CharField(max_length=150,null=True)
    userpic=models.ImageField(upload_to='myimg', null=True ,blank=True)
    regdate=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact=models.CharField(max_length=15, null=True)
    address=models.CharField(max_length=150, null=True)
    userpic = models.ImageField(upload_to='volunteer', null=True, blank=True)
    idpic= models.ImageField(upload_to='volunteer', null=True, blank=True)
    aboutme=models.CharField(max_length=150,null=True)
    status=models.CharField(max_length=20,default='Pending')
    regdate=models.DateTimeField(auto_now_add=True)
    adminremark=models.CharField(max_length=300,null=True)
    updationdate=models.DateTimeField(null=True)

    def __str__(self):
        return self.user.username


class DonationArea(models.Model):
    areaname=models.CharField(max_length=100)
    description=models.CharField(max_length=300)
    creationdate=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.areaname
DONATION_CHOICES=(
    ('Food Donation','Food Donation'),
    ('Cloth Donation','Cloth Donation'),
    ('Shoes Donation','Shoes Donation'),
    ('Books Donation','Books Donation'),
    ('Furniture Donation','Furniture Donation'),
    ('Home Donate','Home Donate'),
    ('Frig Donation','Frig Donation'),
    ('Byc Donation','Byc Donation'),
    ('Others','Others'),
)

DONATION_STATUS=(
        ('Pending', 'Pending'),
        ('Accept', 'Accept'),
        ('Reject', 'Reject'),
        ('Volunteer Allocated', 'Volunteer Allocated'),
        ('Volunteer Not Allocated', 'Volunteer Not Allocated'),
        ('Donation Received','Donation Received'),
        ('Donation Not Received','Donation Not Received'),
        ('Donation Delivered Successfully', 'Donation Delivered Successfully'),
    )
class Donation(models.Model):
    donor=models.ForeignKey(Donor,on_delete=models.CASCADE,null=True)
    donationname=models.CharField(choices=DONATION_CHOICES,max_length=20, null=True)
    donationpic=models.ImageField(upload_to='donation' , null=True, blank=True)
    collectionAddress=models.CharField(max_length=120, null=True)
    description=models.CharField(max_length=120 , null=True)
    status=models.CharField(choices=DONATION_STATUS, max_length=50,default='Pending')
    donationdate=models.DateTimeField(null=True,auto_now_add=True)
    adminremark=models.CharField(max_length=128 ,null=True)
    volunteer=models.ForeignKey(Volunteer,on_delete=models.CASCADE , null=True)
    donationarea=models.ForeignKey(DonationArea,on_delete=models.CASCADE ,null=True)
    volunteerremark=models.CharField(max_length=128,null=True)
    updationdate=models.DateTimeField(null=True)




class Gallery(models.Model):
    donation=models.ForeignKey(Donation,on_delete=models.CASCADE)
    deliverypic=models.FileField(null=True)
    creationdate=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id



