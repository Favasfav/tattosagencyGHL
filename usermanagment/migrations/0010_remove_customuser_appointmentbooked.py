# Generated by Django 5.1.4 on 2024-12-27 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagment', '0009_appointment_assigned_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='appointmentbooked',
        ),
    ]