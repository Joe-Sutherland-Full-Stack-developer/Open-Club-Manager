from django import forms
from .models import Participant

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'date_of_birth', 'emergency_contact_name', 'emergency_contact_number','address','email','additional_info']