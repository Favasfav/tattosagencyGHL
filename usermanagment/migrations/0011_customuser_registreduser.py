# Generated by Django 5.1.4 on 2024-12-27 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagment', '0010_remove_customuser_appointmentbooked'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='registreduser',
            field=models.BooleanField(default=False),
        ),
    ]
