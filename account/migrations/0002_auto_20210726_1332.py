# Generated by Django 3.1.8 on 2021-07-26 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrator',
            name='photo',
            field=models.ImageField(blank=True, default='../static/images/avatar.png', null=True, upload_to='administrator_photos/', verbose_name="Administrator's photo(optional)"),
        ),
    ]
