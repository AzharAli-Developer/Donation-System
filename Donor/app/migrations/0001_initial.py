# Generated by Django 4.2.14 on 2024-07-24 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donationname', models.CharField(choices=[('Food Donation', 'Food Donation'), ('Cloth Donation', 'Cloth Donation'), ('Footwear Donation', 'Footwear Donation'), ('Books Donation', 'Books Donation'), ('Furniture Donation', 'Furniture Donation'), ('Vessel Donation', 'Vessel Donation'), ('Others', 'Others')], max_length=20, null=True)),
                ('donationpic', models.ImageField(blank=True, null=True, upload_to='donation')),
                ('collectionAddress', models.CharField(max_length=120, null=True)),
                ('description', models.CharField(max_length=120, null=True)),
                ('status', models.CharField(choices=[('Accept', 'Accept'), ('Reject', 'Reject')], default='Pending', max_length=20)),
                ('donationdate', models.DateTimeField(auto_now_add=True, null=True)),
                ('adminremark', models.CharField(max_length=128, null=True)),
                ('volunteerremark', models.CharField(max_length=128, null=True)),
                ('updationdate', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DonationArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('areaname', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
                ('creationdate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=15, null=True)),
                ('address', models.CharField(max_length=150, null=True)),
                ('userpic', models.ImageField(blank=True, null=True, upload_to='volunteer')),
                ('idpic', models.ImageField(blank=True, null=True, upload_to='volunteer')),
                ('aboutme', models.CharField(max_length=150, null=True)),
                ('status', models.CharField(max_length=20, null=True)),
                ('regdate', models.DateTimeField(auto_now_add=True)),
                ('adminremark', models.CharField(max_length=300, null=True)),
                ('updationdate', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deliverypic', models.FileField(null=True, upload_to='')),
                ('creationdate', models.DateTimeField(auto_now_add=True)),
                ('donation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.donation')),
            ],
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.IntegerField(null=True)),
                ('address', models.CharField(max_length=150, null=True)),
                ('userpic', models.ImageField(blank=True, null=True, upload_to='myimg')),
                ('regdate', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='donation',
            name='donationarea',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.donationarea'),
        ),
        migrations.AddField(
            model_name='donation',
            name='donor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.donor'),
        ),
        migrations.AddField(
            model_name='donation',
            name='volunteer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.volunteer'),
        ),
    ]
