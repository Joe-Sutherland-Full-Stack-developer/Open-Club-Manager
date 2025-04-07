from django import forms
from django.contrib.auth import get_user_model
import json
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.shortcuts import HttpResponse
from .models import (
    Participant,
    ClassInstance,
    ClassType,
    Booking,
    ContactRequest,
    Timetable,
)

User = get_user_model()


class ParticipantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Check if the field is a visible input field
            if isinstance(field.widget, forms.widgets.Input):
                # Add class to hide input fields
                field.widget.attrs['class'] = ('edit-form-input'
                                               ' d-none')

    class Meta:
        model = Participant
        fields = [
            'first_name', 'last_name', 'date_of_birth',
            'address', 'email', 'emergency_contact_name',
            'emergency_contact_number', 'additional_info'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'additional_info': forms.TextInput(attrs={
                                'class': 'edit-form-input d-none'
                                })
        }


class NewParticipant(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            'first_name', 'last_name', 'date_of_birth',
            'address', 'email', 'emergency_contact_name',
            'emergency_contact_number', 'additional_info'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'date_of_birth': 'Date of Birth',
            'address': 'Address (optional)',
            'email': 'Email Address (optional)',
            'emergency_contact_name': 'Emergency Contact Name',
            'emergency_contact_number': 'Emergency Contact Number',
            'additional_info': ('Additional / Medical Information'
                                ' (optional)')
        }


# class AddEvent(forms.ModelForm):
#     class_type = forms.ModelChoiceField(queryset=ClassType.objects.all(),
#                                         label='Class Type')
#     repeat = forms.BooleanField(required=False, initial=False,
#                                 label="Repeat?")

#     class Meta:
#         model = ClassInstance
#         fields = ['class_type', 'start_time', 'finish_time',
#                   'day', 'repeat']
#         widgets = {
#             "start_time": TimePickerInput(
#                 attrs={'class': 'form-control'},
#                 options=FlatpickrOptions(
#                     time_24hr=True,
#                     minuteIncrement=15
#                 )
#             ),
#             "finish_time": TimePickerInput(
#                 attrs={'class': 'form-control'},
#                 options=FlatpickrOptions(
#                     time_24hr=True,
#                     minuteIncrement=15
#                 )
#             ),
#         }


class BookingForm(forms.ModelForm):
    participant = forms.ModelChoiceField(queryset=Participant.objects.none())
    product_name = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Booking
        fields = ['product_name', 'price', 'participant']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['participant'].queryset = (
                Participant.objects.filter(user=user))


class UserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = ('edit-form-input'
                                                   ' d-none')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4, 'placeholder': 'Your message here...'
                }),
        }


class ClassInstanceForm(forms.ModelForm):
    class_type = forms.ModelChoiceField(queryset=ClassType.objects.all(),
                                        label='Class Type')
    repeat = forms.BooleanField(required=False, initial=False,
                                label="Repeat?")
    repeat_until = forms.DateField(required=False, widget=DatePickerInput(options={"format": "DD/MM/YYYY"}))
    # timetable_id = forms.IntegerField(required=True, widget=forms.HiddenInput(),)
    class Meta:
        model = ClassInstance
        fields = ['class_type', 'day', 'start_time', 'finish_time', 'capacity']
        
        widgets = {
            'start_time': TimePickerInput(options={"format": "HH:mm",
                                                   "stepping": 15}),
            'finish_time': TimePickerInput(options={"format": "HH:mm",
                                                   "stepping": 15}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_type'].widget.attrs.update({
            'class': 'class-type-select',
        })

        # Correctly set up the choices
        class_types = ClassType.objects.all()
        choices = [(ct.id, ct.name) for ct in class_types]  # Value, Label
        self.fields['class_type'].choices = choices

        # Add data attributes to the widget itself
        data_attrs = {
            str(ct.id): {'duration': ct.duration, 'capacity': ct.default_capacity}
            for ct in class_types
        }
        self.fields['class_type'].widget.attrs['data-class-types'] = json.dumps(data_attrs)
        # Remove any initial value to ensure the field starts empty
        self.fields['class_type'].initial = None
        
        self.fields['repeat_until'].widget.attrs['class'] = 'repeat-until-field'
        self.fields['repeat_until'].label_attrs = {'class': 'repeat-until-label'}