# Generated by Django 4.0.4 on 2022-05-29 07:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jumla', '0010_remove_cart_governorate_cart_governorate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='Date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='cart',
            name='Date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]