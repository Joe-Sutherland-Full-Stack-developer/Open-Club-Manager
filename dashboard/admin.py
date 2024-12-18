from django.contrib import admin
from .models import Participant, ClassType, Timetable, ClassInstance, Booking
# Register your models here.
admin.site.register(Participant)
admin.site.register(ClassType)
admin.site.register(Timetable)
admin.site.register(ClassInstance)
admin.site.register(Booking)
