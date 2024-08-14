# Generated by Django 5.0.7 on 2024-07-24 13:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_profile_bonus_rate_alter_profile_modified_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bonus_rate',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Enter bonus rate as format "0.03".', max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(limit_value=0, message='Bonus rate must be a positive number.'), django.core.validators.MaxValueValidator(limit_value=1, message='Bonus rate must not exceed 1.0')], verbose_name='Bonus Rate'),
        ),
    ]
