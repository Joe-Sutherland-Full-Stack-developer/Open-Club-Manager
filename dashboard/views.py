from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import ParticipantForm
from .models import ClassInstance
# Create your views here.

class HomePage(TemplateView):
    """
    Displays home page"
    """
    template_name = 'index.html'

@login_required(login_url='/login/')
def dashboard(request):
    class_instances = ClassInstance.objects.all()
    context = {
        'class_instances': class_instances
    }
    return render(request, 'dashboard/dashboard.html')

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