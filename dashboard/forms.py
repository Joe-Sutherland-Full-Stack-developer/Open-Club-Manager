from django import forms
from .models import Participant, ClassInstance, ClassType
from .models import Timetable
from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name','last_name', 'date_of_birth', 'address','email', 'emergency_contact_name', 'emergency_contact_number', 'additional_info']
        widgets = {
           'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class AddEvent(forms.ModelForm):
    class_type = forms.ModelChoiceField(queryset=ClassType.objects.all(), label='Class Type')
    repeat = forms.BooleanField(required=False, initial=False, label="Repeat?")
    
    class Meta:
        model = ClassInstance
        fields = ['class_type', 'start_time', 'finish_time', 'day', 'repeat']  # Include 'day' if needed
        widgets = {
            "start_time": TimePickerInput(
                attrs={'class': 'form-control',},
                options=FlatpickrOptions(
                    time_24hr=True,
                    minuteIncrement=15
                )
            ),
            "finish_time": TimePickerInput(
                attrs={'class': 'form-control'},
                options=FlatpickrOptions(
                    time_24hr=True,
                    minuteIncrement=15
                )
            ),
        }


  
  