# Generated by Django 3.1.8 on 2021-07-26 12:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('park', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='park',
            name='park_closing_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Park's closing time"),
            preserve_default=False,
        ),
    ]
