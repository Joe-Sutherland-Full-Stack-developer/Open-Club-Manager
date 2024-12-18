from django import forms
from .models import Participant

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'date_of_birth', 'address','email', 'emergency_contact_name', 'emergency_contact_number', 'additional_info']
        widgets = {
           'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }