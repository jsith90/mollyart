# Generated by Django 5.1 on 2024-08-17 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_sold_out",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="product", name="quantity", field=models.IntegerField(default=1),
        ),
    ]
