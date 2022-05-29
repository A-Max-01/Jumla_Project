# Generated by Django 4.0.4 on 2022-05-28 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jumla', '0006_alter_product_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill_Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(verbose_name='item_qty')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_item', to='jumla.product')),
            ],
        ),
        migrations.AlterField(
            model_name='bill',
            name='products',
            field=models.ManyToManyField(related_name='bill_products', to='jumla.bill_items'),
        ),
    ]