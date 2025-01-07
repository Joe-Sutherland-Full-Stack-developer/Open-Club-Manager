from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Participant, ClassType, Timetable, ClassInstance, Booking
from django import forms
from .forms import AddEvent

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




class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'participant', 'class_instance', 'paid_or_member', 'created_on', 'updated_on', 'active']
    list_filter = ['paid_or_member', 'active', 'created_on', 'updated_on']
    search_fields = ['id','user__username', 'participant__first_name', 'participant__last_name']
    readonly_fields = ['id', 'created_on', 'updated_on']
    fields = ['user', 'participant', 'class_instance', 'paid_or_member', 'active', 'created_on', 'updated_on']
    actions = ['set_inactive','set_active','mark_as_paid', 'mark_as_not_paid']

    def set_inactive(self, request, queryset):
        queryset.update(active=False, updated_on=timezone.now())
    set_inactive.short_description = "Mark selected bookings as inactive (Use this to cancel bookings without deleting them)"

    def set_active(self, request, queryset):
        # Update the active field to True and set updated_on to now
        queryset.update(active=True, updated_on=timezone.now())
    set_active.short_description = "Mark selected bookings as active"


    def mark_as_paid(self, request, queryset):
        queryset.update(paid_or_member=True, updated_on=timezone.now())
    mark_as_paid.short_description = "Mark selected bookings as paid"
       
    def mark_as_not_paid(self, request, queryset):
        queryset.update(paid_or_member=False, updated_on=timezone.now())
    mark_as_not_paid.short_description = "Mark selected bookings as not paid"

admin.site.register(Booking, BookingAdmin)

#Custom Forms

class TimetableForm(forms.ModelForm):
    # Define the available choices for selection

    
    selected_days = forms.MultipleChoiceField( 
        label= Timetable._meta.get_field("selected_days").verbose_name,
        choices=Timetable.day_choices,
        required=not Timetable._meta.get_field("selected_days").blank,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Timetable
        fields = ['name', 'active', 'selected_days','start_time', 'end_time', 'notes'] 
        widgets = {
            "start_time": TimePickerInput(options={
                    "format": "HH:mm",
                    "stepping": 15,
                    "showClose": True,
                    "showClear": True,
                }
            ),
            "end_time": TimePickerInput(options={
                    "format": "HH:mm",
                    "stepping": 15,
                    "showClose": True,
                    "showClear": True,
                }
            )
        }
            
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['selected_days'].initial = self.instance.selected_days

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.selected_days = self.cleaned_data['selected_days']
        if commit:
            instance.save()
        return instance
    
@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    form = TimetableForm
    list_display = ["__str__"]
    fields = ['name', 'active', 'selected_days','start_time', 'end_time', 'notes']


@admin.register(ClassInstance)
class ClassInstAdmin(admin.ModelAdmin):
    form = AddEvent
    list_display = ["__str__"]
    fields = ['class_type', 'instance_date', 'day', 'start_time', 'finish_time', 'capacity', 'attendees']