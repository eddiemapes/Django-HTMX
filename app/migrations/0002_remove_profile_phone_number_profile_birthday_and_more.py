# Generated by Django 5.0.7 on 2024-07-24 15:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='bonus_rate',
            field=models.FloatField(blank=True, help_text='Enter bonus rate as format "0.03".', null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='department',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='ip_address',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_four_ssn',
            field=models.CharField(blank=True, max_length=4, null=True, validators=[django.core.validators.RegexValidator(message="Enter the last four digits of the user's SSN.", regex='^\\d+$')], verbose_name='Last Four SSN'),
        ),
        migrations.AddField(
            model_name='profile',
            name='mobile_phone',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='Mobile number must be entered as digits only.', regex='^\\d+$')], verbose_name='Mobile Phone'),
        ),
        migrations.AddField(
            model_name='profile',
            name='offer_date',
            field=models.DateField(blank=True, help_text='Enter the date the offer letter was sent.', null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='office_phone',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='Office number must be entered as digits only.', regex='^\\d+$')], verbose_name='Office Phone'),
        ),
        migrations.AddField(
            model_name='profile',
            name='personal_email',
            field=models.EmailField(blank=True, help_text="Enter the user's personal email address.", max_length=254, null=True, verbose_name='Personal Email'),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_extension',
            field=models.CharField(blank=True, max_length=5, null=True, validators=[django.core.validators.RegexValidator(message='Phone extension must be entered as digits only.', regex='^\\d+$')], verbose_name='Phone Extension'),
        ),
        migrations.AddField(
            model_name='profile',
            name='start_date',
            field=models.DateField(blank=True, help_text='Enter the date the user started.', null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.CharField(blank=True, error_messages="Enter the state's abbreviated name.", max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='term_date',
            field=models.DateField(blank=True, help_text="Enter the date the user's employment was terminated.", null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='zip_code',
            field=models.CharField(blank=True, max_length=5, null=True, validators=[django.core.validators.RegexValidator(message='Zip code must be entered as digits only.', regex='^\\d+$')], verbose_name='Zip Code'),
        ),
    ]
