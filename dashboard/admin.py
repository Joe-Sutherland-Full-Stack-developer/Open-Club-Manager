from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Participant, ClassType, Timetable, ClassInstance, Booking

class ParticipantInline(admin.StackedInline):
    model = Participant
    extra = 0

class CustomUserAdmin(UserAdmin):
    inlines = (ParticipantInline,)

# Unregister the default UserAdmin
admin.site.unregister(User)

# Register the new CustomUserAdmin
admin.site.register(User, CustomUserAdmin)

# Register your models here.
admin.site.register(Participant)
admin.site.register(ClassType)
admin.site.register(Timetable)
admin.site.register(ClassInstance)
admin.site.register(Booking)
