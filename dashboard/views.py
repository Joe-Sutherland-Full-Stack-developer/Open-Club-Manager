# Standard library imports
from datetime import timedelta, datetime

# Third-party imports
import stripe
from weasyprint import HTML

# Django imports
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import now
from django.utils.formats import date_format
from django.db.models import Q
from django.views.generic import TemplateView

# Local imports
from .forms import (
    UserEditForm, ParticipantForm, BookingForm, NewParticipant,
    ContactForm, ClassInstanceForm
)
from .models import (
    ClassInstance, Timetable, Booking, Participant, StripeIntegration, ClassType
)
from OpenClubManager.stripe_utils import (
    initialize_stripe
)


class Home(TemplateView):
    """Displays home page"""
    template_name = 'dashboard/home.html'


@login_required(login_url='/accounts/login/')
def dashboard(request):
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    end_of_month = (
                    (today.replace(day=1) + timedelta(days=32))
                    .replace(day=1)
                    - timedelta(days=1)
                    )

    start_of_next_week = end_of_week + timedelta(days=1)
    end_of_next_week = start_of_next_week + timedelta(days=6)
    print(f"End of month var: {end_of_month}")
    class_instances = ClassInstance.objects.filter(
        instance_date__gte=today
    ).order_by('instance_date', 'start_time')
    timetables = Timetable.objects.filter(active=True)

    this_week, next_week, later_this_month, later_this_year = [], [], [], []

    for instance in class_instances:
        if start_of_week <= instance.instance_date <= end_of_week:
            this_week.append(instance)
        elif start_of_next_week <= instance.instance_date <= end_of_next_week:
            next_week.append(instance)
        elif end_of_next_week < instance.instance_date <= end_of_month:
            later_this_month.append(instance)
            print(f"Later this month: {[instance.instance_date for instance in later_this_month]}")
        else:
            later_this_year.append(instance)

    this_week_by_day = {}
    for instance in this_week:
        day_name = instance.instance_date.strftime('%A')
        if day_name not in this_week_by_day:
            this_week_by_day[day_name] = []
        this_week_by_day[day_name].append(instance)

    next_week_by_day = {}
    for instance in next_week:
        day_name = instance.instance_date.strftime('%A')
        if day_name not in next_week_by_day:
            next_week_by_day[day_name] = []
        next_week_by_day[day_name].append(instance)

    context = {
        'user': request.user,
        'this_week_by_day': this_week_by_day,
        'next_week_by_day': next_week_by_day,
        'later_this_month': later_this_month,
        'later_this_year': later_this_year,
        'timetables': timetables,
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='/login/')
def load_booking_form(request, event_id):
    event = get_object_or_404(ClassInstance, id=event_id)
    user = request.user
    form = BookingForm(
        user=request.user,
        initial={
            'class_instance': event,
            'participant': (
                user.participants.first() if user.participants.exists() else None
            ),
        }
    )
    return render(
        request,
        'dashboard/booking_form.html',
        {'form': form, 'event': event, 'user': user}
    )


def create_booking(request):
    user = request.user
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.class_instance_id = request.POST.get('class_instance_id')
            booking.save()
            return redirect('booking_confirmation', booking_id=booking.id)
    return redirect('dashboard')


def booking_owner_or_admin(user, booking):
    return user == booking.user or user.is_staff


def view_bookings(request):
    current_date = timezone.now().date()
    
    upcoming_bookings = Booking.objects.filter(
        user=request.user,
        class_instance__instance_date__gte=current_date,
        active=True
    )
    
    previous_bookings = Booking.objects.filter(
        Q(user=request.user) &
        (Q(class_instance__instance_date__lt=current_date) | Q(active=False))
    )
    
    return render(
        request,
        'dashboard/view_bookings.html',
        {
            'upcoming_bookings': upcoming_bookings,
            'previous_bookings': previous_bookings,
        }
    )



@login_required
def create_participant(request):
    if request.method == 'POST':
        form = NewParticipant(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.user = request.user
            participant.save()
            messages.success(request, "Participant created successfully.")
            return redirect('account_details')
    else:
        form = NewParticipant()
    return render(request, 'dashboard/create_participant.html', {'form': form})

from .forms import ClassInstanceForm

def get_class_form(request):
    form = ClassInstanceForm()
    return render(request, 'class_form.html', {'form': form})

@login_required
def add_class_instance(request):
    if request.method == 'POST':
        form = ClassInstanceForm(request.POST)
        if form.is_valid():
            # Get the selected day from the form
            selected_day = form.cleaned_data['day']
            
            # Calculate instance_date based on selected_day
            instance_date = get_date_for_day_of_week(selected_day)

            # Assign the calculated date to the form's instance_date field
            form.instance.instance_date = instance_date

            # get timetable id from the form
            timetable_id = request.POST.get('timetable_id')
            timetable = get_object_or_404(Timetable, id=timetable_id)
            form.instance.timetable = timetable

            class_instance = form.save()
            messages.success(request, "Class added successfully!")
            # Handle repeats
            if form.cleaned_data.get('repeat'):
                repeat_until = form.cleaned_data['repeat_until']
                    
                # Validate repeat_until date
                if not repeat_until or repeat_until <= instance_date:
                    form.add_error('repeat_until', 'Invalid repeat date')
                    return JsonResponse({'success': False, 'error': form.errors.as_json()}, status=400)
                    
                # Calculate weekly dates and bulk create
                days_diff = (repeat_until - instance_date).days
                num_repeats = days_diff // 7
                    
                instances = [
                    ClassInstance(
                        timetable=timetable,
                        class_type=class_instance.class_type,
                        instance_date=instance_date + timedelta(weeks=i+1),
                        day=selected_day,
                        start_time=class_instance.start_time,
                        finish_time=class_instance.finish_time,
                        capacity=class_instance.capacity
                    )
                    for i in range(num_repeats)
                ]
                ClassInstance.objects.bulk_create(instances)
                # Notify user of successful repeat creation
                
                repeat_until_str = f"{date_format(repeat_until, 'DATE_FORMAT')}"
                messages.success(request, f"Successfully set class to repeat weekly until {repeat_until_str}")
                
                
            # Redirect to HTTP_REFERER (previous page)
            referer_url = request.META.get('HTTP_REFERER', '/dashboard')  # Fallback to '/dashboard' if no referer
            return redirect(referer_url)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'error': errors}, status=400)
    else:
        form = ClassInstanceForm()
    return render(request, 'dashboard/timetable.html', {'form': form})

def get_date_for_day_of_week(day_name):
    days_of_week = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    today = datetime.now().date()
    day_index = days_of_week.index(day_name)
    current_day = today.weekday()  # Monday is 0, Sunday is 6
    diff = day_index - current_day

    if diff < 0:
        diff += 7

    instance_date = today + timedelta(days=diff)

    return instance_date

def timetable_view(request, timetable_id):
    timetable = get_object_or_404(Timetable, id=timetable_id, active=True)
    
    selected_days = timetable.selected_days
    time_slots = timetable.time_slots

    class_instances = ClassInstance.objects.filter(
        start_time__gte=timetable.start_time,
        finish_time__lte=timetable.end_time,
        instance_date__gte=timezone.now().date()  # Filter instances with instance_date after today
    ).select_related('class_type').order_by('day', 'start_time')
    form = ClassInstanceForm
    context = {
        'timetable': timetable,
        'selected_days': selected_days,
        'time_slots': time_slots,
        'class_instances': class_instances,
        'form': form,
    }

    return render(request, 'dashboard/timetable.html', context)



def booking_confirmation_pdf(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    html_string = render_to_string(
        'booking_confirmation_pdf.html', {'booking': booking}
        )
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="booking_confirmation_{booking.id}.pdf"'
        )
    HTML(string=html_string).write_pdf(response)
    return response

@require_POST
def CancelBookingView(request, booking_id):
    if request.method == 'POST':
        # Handle the cancellation
        booking = get_object_or_404(Booking, id=booking_id)
        booking.active = False
        booking.save()
        return redirect('view_bookings')  # Correct the redirect URL as needed

@login_required
def account_details(request):
    if request.method == 'POST':
        if 'participant_id' in request.POST:  
            participant_id = request.POST.get('participant_id')
            field_name = request.POST.get(
                                          'field_name'
                                          )  # Get field name from POST data
            value = request.POST.get(
                                     field_name
                                     )  # Get the value for the specific field
            form = ParticipantForm(request.POST)
            print("Updating participant:", participant_id,
                  "Field:", field_name, "Value:", value)  # Debugging output
            if form.is_valid():
                try:
                    # Get the existing participant instance
                    participant = Participant.objects.get(
                        id=participant_id, user=request.user
                        )
                    # Update participant fields with cleaned data from the form
                    for field in form.cleaned_data:
                        setattr(participant, field, form.cleaned_data[field])

                    participant.save()

                    messages.success(request,
                                     "Participant updated successfully."
                                     )
                except Participant.DoesNotExist:
                    messages.error(request,
                                   "Participant does not exist."
                                   )
                except Exception as e:
                    messages.error(request,
                                   f"Error updating participant: {str(e)}"
                                   )  # Catch any other exceptions

                return redirect('account_details')

        else:  # Handle user form submission
            form = UserEditForm(request.POST, instance=request.user)
            if form.is_valid():
                field_name = request.POST.get('field_name')
                if field_name in form.fields:
                    setattr(request.user, field_name, 
                            form.cleaned_data[field_name])
                    request.user.save()
                return redirect('account_details')

    else:  # GET request: initialize forms and get participants
        form = UserEditForm(instance=request.user)
        participants = request.user.participants.all()
        participant_forms = [ParticipantForm(instance=participant) 
                             for participant in participants]
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
    participant = get_object_or_404(Participant,
                                    id=participant_id,
                                    user=request.user)
    participant.delete()
    messages.success(request, "Participant deleted successfully.")
    return redirect('account_details')


def home(request):
    return render(request, 'dashboard/home.html')


def create_checkout_session(request):
    stripe_publishable_key = initialize_stripe()

    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            price = int(form.cleaned_data['price'] * 100)
            class_instance_id = request.POST.get('class_instance_id')

            booking = Booking.objects.create(
                user=request.user,
                participant=form.cleaned_data['participant'],
                class_instance_id=class_instance_id,
                paid_or_member=False
            )
            stripe_settings = StripeIntegration.objects.first()
            currency = stripe_settings.currency
            print(currency)
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': currency,
                                'unit_amount': price,
                                'product_data': {
                                    'name': product_name,
                                },
                            },
                            'quantity': 1,
                        },
                    ],
                    mode='payment',
                    success_url=request.build_absolute_uri(
                        f'/booking-confirmation/{booking.id}/'
                    ),
                    cancel_url=request.build_absolute_uri(
                        '/booking-cancelled/'),
                )
                return redirect(checkout_session.url)
            except Exception as e:
                print(f"Error creating checkout session: {str(e)}")
                return render(request, 'dashboard/error.html',
                              {'error': str(e)})
        else:
            print(form.errors)
            return render(request, 'dashboard/booking_form.html',
                          {'form': form})
    else:
        form = BookingForm(user=request.user)
        return render(request, 'dashboard/booking_form.html',
                      {'form': form})


def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.paid_or_member = True
    booking.save()
    return render(request, 'dashboard/booking_confirmation.html',
                  {'booking': booking})


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():  # Check if the form is valid
            contact_request = form.save(commit=False)  # Create an instance but don't save to DB yet
            if request.user.is_authenticated:
                contact_request.user = request.user  # Assign the user if logged in
            contact_request.save()  # Now save the instance to the database
            return redirect('contact_success')  # Redirect after successful submission
    return render(request, 'dashboard/contact.html', {'form': form})

class ContactSuccess(TemplateView):
    template_name = 'dashboard/contact_success.html'


class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if not Participant.objects.filter(user=user).exists():
            return redirect('create_participant')
        return super().form_valid(form)
    

def contact_success(request):
    return render(request, 'dashboard/contact_success.html') 