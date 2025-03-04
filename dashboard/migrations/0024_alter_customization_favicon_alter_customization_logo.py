# Generated by Django 4.2.17 on 2025-02-22 20:02

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0023_classtype_members_only"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customization",
            name="favicon",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="favicon"
            ),
        ),
        migrations.AlterField(
            model_name="customization",
            name="logo",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="logo"
            ),
        ),
    ]
