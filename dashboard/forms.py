from django import forms
from .models import Participant
from .models import Timetable

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



    
  