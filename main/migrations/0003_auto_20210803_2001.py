# Generated by Django 3.1.8 on 2021-08-03 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_listing'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Listing',
            new_name='Waitlist',
        ),
    ]