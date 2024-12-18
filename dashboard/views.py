from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import ParticipantForm
# Create your views here.

class HomePage(TemplateView):
    """
    Displays home page"
    """
    template_name = 'index.html'


def create_participant(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.user = request.user
            participant.save()
            return redirect('home')
    else:
        form = ParticipantForm()
        context = {
            'form': form,
        }
        return render(request, 'dashboard/create_participant.html', context)