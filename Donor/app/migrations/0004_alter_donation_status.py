# Generated by Django 4.2.14 on 2024-07-28 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_donation_donationname_alter_volunteer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accept', 'Accept'), ('Volunteer Allocated', 'Volunteer Allocated'), ('Volunteer Not Allocated', 'Volunteer Not Allocated'), ('Delievered Successfully', 'Delievered Successfully')], default='Pending', max_length=50),
        ),
    ]
