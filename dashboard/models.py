from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class ClassType(models.Model):
    duration_choices = ((15, '15 Minutes'), (30, '30 Minutes'),
                        (45, '45 Minutes'), (60, '1 Hour'),
                        (75, '1 Hour 15 Minutes'), (90, '1 Hour 30 Minutes'),
                        (105, '1 hour 45 Minutes'), (120, '2 Hours'),
                        (135, '2 Hours 15 Minutes'), (150, '2 Hours 30 Minutes'),
                        (165, '2 Hours 45 Minutes'), (180, '3 Hours'),
                        (195, '3 Hours 15 Minutes'), (210, '3 Hours 30 Minutes'),
                        (225, '3 Hours 45 Minutes'), (240, '4 Hours'),
                        (255, '4 Hours 15 Minutes'), (270, '4 Hours 30 Minutes'),
                        (285, '4 Hours 45 Minutes'), (300, '5 Hours'))
    name = models.CharField(max_length=100)
    age_group_min = models.IntegerField()
    age_group_max = models.IntegerField(default=99)
    duration = models.IntegerField(choices = duration_choices)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    default_capacity = models.IntegerField(default=0)

class Timetable(models.Model):
    day_choices = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    selected_days = models.JSONField(
    default=list,
    help_text="Store selected days of the week as a JSON array (e.g., ['MON', 'TUE'])"
    )

    start_time = models.TimeField()
    end_time = models.TimeField()
    notes = models.TextField(blank=True)

class ClassInstance(models.Model):
    class_type = models.ForeignKey('ClassType', on_delete=models.CASCADE)
    instance_date = models.DateTimeField()
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    capacity = models.IntegerField(0)
    attendees = models.ManyToManyField('Booking')

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE)
    class_instance = models.ForeignKey('ClassInstance', on_delete=models.CASCADE)
    paid_or_member = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

class Participant(models.Model):
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    is_member = models.BooleanField(default=False)
    address = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_number = models.CharField(max_length=15)
    additional_info = models.TextField(null=True, blank=True)
    