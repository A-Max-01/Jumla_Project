# Generated by Django 4.0.4 on 2022-05-31 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jumla', '0007_remove_bill_quantity_remove_cart_governorate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
