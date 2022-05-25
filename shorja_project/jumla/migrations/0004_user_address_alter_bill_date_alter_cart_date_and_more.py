# Generated by Django 4.0.4 on 2022-05-25 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jumla', '0003_alter_category_options_alter_bill_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='Date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='cart',
            name='Date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='Date',
            field=models.DateTimeField(),
        ),
    ]
