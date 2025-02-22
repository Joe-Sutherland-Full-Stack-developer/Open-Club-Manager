# Generated by Django 4.2.17 on 2025-01-05 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_rename_name_participant_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='selected_days',
            field=models.JSONField(help_text="Store selected days of the week as a JSON array (e.g., ['MON', 'TUE'])"),
        ),
    ]
