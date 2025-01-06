from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta, datetime
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import ParticipantForm, AddEvent
from .models import ClassInstance, Timetable
from bootstrap_datepicker_plus.widgets import TimePickerInput

# Create your views here.

class HomePage(TemplateView):
    """
    Displays home page"
    """
    template_name = 'index.html'


@login_required(login_url='/login/')
def dashboard(request):
    timetable_instance = get_object_or_404(Timetable, active = True)
    class_instances = ClassInstance.objects.filter()

    context = {
        'user': request.user,
        'timetable': timetable_instance,
        'class_instances': class_instances,
    }   
        
    return render(request, 'dashboard/dashboard.html', context)

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

def timetable_view(request, timetable_id):
    timetable_instance = get_object_or_404(Timetable, id=timetable_id)
    form = AddEvent()
    print("Form data:", request.POST)  # Print out the raw POST data

    # Get the current date
    today = timezone.now().date()

    # Calculate the start and end of the current week
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    # Fetch class instances for the current week
    class_instances = ClassInstance.objects.filter(
        instance_date__range=(start_of_week, end_of_week)
    ).order_by('instance_date')
    
    if request.method == "POST":
        form = AddEvent(request.POST)
        if form.is_valid():
            class_type = form.cleaned_data['class_type']
            start_time = form.cleaned_data['start_time']  # This is a time object
            finish_time = form.cleaned_data['finish_time']  # This is a time object
            day_of_week = form.cleaned_data['day']
            repeat = form.cleaned_data.get('repeat', False)
            
            day_map = {'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4, 'SAT': 5, 'SUN': 6}
            
            today = timezone.now().date()
            target_weekday = day_map[day_of_week]
            days_ahead = (target_weekday - today.weekday() + 7) % 7
            
            if days_ahead == 0:
                days_ahead += 7
            
            next_date = today + timedelta(days=days_ahead)
            
            # Combine date and time to create timezone-aware datetimes
            start_datetime = timezone.make_aware(datetime.combine(next_date, start_time))
            finish_datetime = timezone.make_aware(datetime.combine(next_date, finish_time))
            
            # Create initial instance
            ClassInstance.objects.create(
                class_type=class_type,
                instance_date=next_date,
                start_time=start_datetime,
                finish_time=finish_datetime,
                day = day_of_week
            )

            # If repeat is checked, create additional instances for the next three weeks
            if repeat:
                for i in range(1, 4):  # Create three additional instances
                    next_date += timedelta(weeks=1)
                    start_datetime = timezone.make_aware(datetime.combine(next_date, start_time))
                    finish_datetime = timezone.make_aware(datetime.combine(next_date, finish_time))
                    
                    ClassInstance.objects.create(
                        class_type=class_type,
                        instance_date=next_date,
                        start_time=start_datetime,
                        finish_time=finish_datetime,
                        day = day_of_week
                    )

            return redirect('timetable_view', timetable_id=timetable_instance.id)
        else:
            print("Form errors:", form.errors)

    context = {
        'timetable': timetable_instance,
        'form': form,
        'timetable_id': timetable_instance.id,
        'class_instances': class_instances, 
        
    }
    
    return render(request, 'dashboard/timetable.html', context)


