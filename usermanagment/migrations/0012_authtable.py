# Generated by Django 5.1.4 on 2024-12-27 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagment', '0011_customuser_registreduser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authtable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_id', models.CharField(unique=True)),
                ('access_token', models.CharField()),
                ('refresh_token', models.CharField()),
                ('expires_in', models.DateTimeField()),
            ],
        ),
    ]