# Generated by Django 5.1.4 on 2024-12-31 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagment', '0014_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='session_no',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
