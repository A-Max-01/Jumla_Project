# Generated by Django 4.0.4 on 2022-05-27 09:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('jumla', '0004_user_address_alter_bill_date_alter_cart_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 27, 9, 57, 4, 97377, tzinfo=utc)),
        ),
    ]
