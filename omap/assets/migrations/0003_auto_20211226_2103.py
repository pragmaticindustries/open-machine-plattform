# Generated by Django 3.1 on 2021-12-26 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0002_assetrelation_relationtype"),
    ]

    operations = [
        migrations.AlterField(
            model_name="relationtype",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
