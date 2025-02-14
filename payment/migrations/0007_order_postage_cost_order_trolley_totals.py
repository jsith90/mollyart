# Generated by Django 5.1 on 2024-10-17 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0006_orderitem_is_size_orderitem_size"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="postage_cost",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=7, null=True
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="trolley_totals",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=7, null=True
            ),
        ),
    ]
