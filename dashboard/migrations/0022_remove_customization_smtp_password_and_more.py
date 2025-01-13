# Generated by Django 4.2.17 on 2025-01-13 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_customization_contact_address_1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customization',
            name='smtp_password',
        ),
        migrations.RemoveField(
            model_name='customization',
            name='smtp_port',
        ),
        migrations.RemoveField(
            model_name='customization',
            name='smtp_server',
        ),
        migrations.RemoveField(
            model_name='customization',
            name='smtp_username',
        ),
        migrations.AlterField(
            model_name='customization',
            name='business_name',
            field=models.CharField(default='Open Club Manager', max_length=200),
        ),
    ]
