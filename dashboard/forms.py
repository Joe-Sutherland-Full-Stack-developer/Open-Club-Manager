from django import forms
from .models import Participant, ClassInstance, ClassType, Booking, ContactRequest
from .models import Timetable
from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.contrib.auth import get_user_model

class ParticipantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
            # Check if the field is a visible input field and not a label or non-input widget
                if isinstance(field.widget, forms.widgets.Input):
                    field.widget.attrs['class'] = 'edit-form-input d-none'  # Add class to hide input fields

    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'date_of_birth', 'address', 'email', 
                  'emergency_contact_name', 'emergency_contact_number', 'additional_info']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'additional_info': forms.TextInput(attrs={'class': 'edit-form-input d-none'})
        }
    
class NewParticipant(forms.ModelForm):

    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'date_of_birth', 'address', 'email', 
                  'emergency_contact_name', 'emergency_contact_number', 'additional_info']
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


class BookingForm(forms.ModelForm):
    participant = forms.ModelChoiceField(queryset=None)
    class Meta:
        model = Booking
        fields = [ 'participant',]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['participant'].queryset = Participant.objects.filter(user=user)

User= get_user_model()
class UserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'edit-form-input d-none'  # or any other class
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email', 'message']  # Exclude 'user' and 'created_on'
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your message here...'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address'}),
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
        }