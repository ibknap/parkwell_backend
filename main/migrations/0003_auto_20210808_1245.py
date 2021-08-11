# Generated by Django 3.1.8 on 2021-08-08 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        ('main', '0002_auto_20210808_1206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='navigate',
            options={'verbose_name': 'Navigate', 'verbose_name_plural': 'Navigates'},
        ),
        migrations.AddField(
            model_name='navigate',
            name='company',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='company.company'),
            preserve_default=False,
        ),
    ]