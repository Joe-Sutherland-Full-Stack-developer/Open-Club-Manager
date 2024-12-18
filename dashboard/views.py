from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class HomePage(TemplateView):
    """
    Displays home page"
    """
    template_name = 'index.html'


def create_participant(request):
    if request.method == 'POST':
        pass
    else:
        pass