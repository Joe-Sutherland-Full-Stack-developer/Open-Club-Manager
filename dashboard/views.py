from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta, datetime
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import ParticipantForm, AddEvent, BookingForm, NewParticipant
from .models import ClassInstance, Timetable, Booking, Participant
from bootstrap_datepicker_plus.widgets import TimePickerInput
from datetime import datetime, timedelta
from django.utils.timezone import now
from weasyprint import HTML
# Create your views here.

class home(TemplateView):
    """
    Displays home page"
    """
    template_name = 'dashboard/home.html'


@login_required(login_url='/login/')
def dashboard(request):
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week
    end_of_week = start_of_week + timedelta(days=6)  # Sunday of the current week
    end_of_month = (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    start_of_next_week = end_of_week + timedelta(days=1)  # Monday of next week
    end_of_next_week = start_of_next_week + timedelta(days=6)  # Sunday of next week
    
    class_instances = ClassInstance.objects.filter(instance_date__gte=today).order_by('instance_date', 'start_time')
    timetables = Timetable.objects.filter(active=True)
    # Group events into categories
    this_week = []
    next_week = []
    later_this_month = []
    later_this_year = []

    for instance in class_instances:
        if start_of_week <= instance.instance_date <= end_of_week:
            this_week.append(instance)
        elif start_of_next_week <= instance.instance_date <= end_of_next_week:
            next_week.append(instance)
        elif instance.instance_date <= end_of_month:
            later_this_month.append(instance)
        else:
            later_this_year.append(instance)

    # Organize this week's events by day
    this_week_by_day = {}
    for instance in this_week:
        day_name = instance.instance_date.strftime('%A')  # e.g., "Tuesday"
        if day_name not in this_week_by_day:
            this_week_by_day[day_name] = []
        this_week_by_day[day_name].append(instance)

    # Organize next week's events by day
    next_week_by_day = {}
    for instance in next_week:
        day_name = instance.instance_date.strftime('%A')  # e.g., "Tuesday"
        if day_name not in next_week_by_day:
            next_week_by_day[day_name] = []
        next_week_by_day[day_name].append(instance)
    context = {
        'user': request.user,
        'this_week_by_day': this_week_by_day,
        'next_week_by_day': next_week_by_day,
        'later_this_month': later_this_month,
        'later_this_year': later_this_year,
        'timetables' : timetables,
        
    }

    return render(request, 'dashboard/dashboard.html', context)



@login_required(login_url='/login/')
def load_booking_form(request, event_id):
    event = get_object_or_404(ClassInstance, id=event_id)
    user = request.user
    form = BookingForm( user=request.user, initial={
        'class_instance': event,
        'participant': user.participants.first,
        
      
    })
    return render(request, 'dashboard/booking_form.html', {'form': form, 'event': event})


def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.class_instance_id = request.POST.get('class_instance_id')
            booking.save()
            
            # Redirect to the booking confirmation page with the new booking ID
            return redirect('booking_confirmation', booking_id=booking.id)

    # Redirect to dashboard or handle failure case
    return redirect('dashboard')  # or wherever you want to redirect on failure

def booking_owner_or_admin(user, booking):
    return user == booking.user or user.is_staff

# Check if the user is the owner of the booking or an admin
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if not booking_owner_or_admin(request.user, booking):
        return HttpResponseForbidden("You do not have permission to view this booking.")

    return render(request, 'dashboard/booking_confirmation.html', {'booking': booking})


def view_bookings(request):
    current_date = timezone.now().date()
    upcoming_bookings = Booking.objects.filter(user=request.user, class_instance__instance_date__gte=current_date)
    previous_bookings = Booking.objects.filter(user=request.user, class_instance__instance_date__lt=current_date)

    return render(request, 'dashboard/view_bookings.html', {'upcoming_bookings': upcoming_bookings,
        'previous_bookings': previous_bookings,})


@login_required
def create_participant(request):
    if request.method == 'POST':
        form = NewParticipant(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.user = request.user  # Associate with logged-in user
            participant.save()
            messages.success(request, "Participant created successfully.")
            return redirect('account_details')  # Redirect after saving
    else:
        form = NewParticipant()  # Initialize an empty form for GET requests

    return render(request, 'dashboard/create_participant.html', {'form': form})
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

def booking_confirmation_pdf(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    html_string = render_to_string('booking_confirmation_pdf.html', {'booking': booking})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="booking_confirmation_{booking.id}.pdf"'
    HTML(string=html_string).write_pdf(response)
    return response



#---------------------------------------------------------------------- Testing area


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from .forms import UserEditForm
from django.contrib import messages

@login_required
def account_details(request):
    if request.method == 'POST':
        if 'participant_id' in request.POST:  # Handle participant form submission
            participant_id = request.POST.get('participant_id')
            field_name = request.POST.get('field_name')  # Get field name from POST data
            value = request.POST.get(field_name)  # Get the value for the specific field

            print("Updating participant:", participant_id, "Field:", field_name, "Value:", value)  # Debugging output

            try:
                # Get the existing participant instance
                participant = Participant.objects.get(id=participant_id, user=request.user)
                setattr(participant, field_name, value)  # Update the specific field
                participant.save()  # Save changes to the existing participant
                messages.success(request, "Participant updated successfully.")  # Optional success message
            except Participant.DoesNotExist:
                messages.error(request, "Participant does not exist.")  # Handle error case
            except Exception as e:
                messages.error(request, f"Error updating participant: {str(e)}")  # Catch any other exceptions

            return redirect('account_details')  # Redirect back after processing

        else:  # Handle user form submission
            form = UserEditForm(request.POST, instance=request.user)
            if form.is_valid():
                field_name = request.POST.get('field_name')
                if field_name in form.fields:
                    setattr(request.user, field_name, form.cleaned_data[field_name])
                    request.user.save()
                return redirect('account_details')

    else:  # GET request: initialize forms and get participants
        form = UserEditForm(instance=request.user)
        participants = request.user.participants.all()
        participant_forms = [ParticipantForm(instance=participant) for participant in participants]
        new_parti_form = NewParticipant()

    context = {
        'form': form,
        'participant_forms': participant_forms,
        'participants': participants,
        'new_parti_form': new_parti_form,
    }

    return render(request, 'dashboard/account_details.html', context)



@login_required
def delete_participant(request, participant_id):
    participant = get_object_or_404(Participant, id=participant_id, user=request.user)
    participant.delete()  # Delete the participant
    messages.success(request, "Participant deleted successfully.")  # Optional success message
    return redirect('account_details')  # Redirect back to account details or wherever appropriate


def home(request):
    return render(request,'dashboard/home.html',)