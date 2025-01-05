from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Participant, ClassType, Timetable, ClassInstance, Booking
from django import forms

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

admin.site.register(ClassInstance)
admin.site.register(Booking)


#Custom Forms

class TimetableForm(forms.ModelForm):
    # Define the available choices for selection

    
    selected_days = forms.MultipleChoiceField( 
        label= Timetable._meta.get_field("selected_days").verbose_name,
        choices=Timetable.day_choices,
        required=not Timetable._meta.get_field("selected_days").blank,
        widget=forms.CheckboxSelectMultiple(),
    )

    start_time = forms.TimeInput()

    class Meta:
        model = Timetable
        fields = ['name', 'active', 'selected_days','start_time', 'end_time', 'notes'] 

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