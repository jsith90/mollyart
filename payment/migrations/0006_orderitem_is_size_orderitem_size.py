# Generated by Django 5.1 on 2024-09-25 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0005_order_payment_method"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="is_size",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="size",
            field=models.CharField(
                blank="True", default=None, max_length=300, null="True"
            ),
            preserve_default="True",
        ),
    ]