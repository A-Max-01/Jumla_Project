# Generated by Django 4.0.4 on 2022-06-10 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jumla', '0014_alter_bill_items_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill_items',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_item', to='jumla.product'),
        ),
    ]