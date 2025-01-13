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
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import now
from django.views.generic import TemplateView

# Local imports
from .forms import (
    UserEditForm, ParticipantForm, AddEvent, BookingForm, NewParticipant,
    ContactForm
)
from .models import (
    ClassInstance, Timetable, Booking, Participant, StripeIntegration
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
        elif instance.instance_date <= end_of_month:
            later_this_month.append(instance)
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
        class_instance__instance_date__gte=current_date
    )
    previous_bookings = Booking.objects.filter(
        user=request.user,
        class_instance__instance_date__lt=current_date
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


def timetable_view(request, timetable_id):
    timetable_instance = get_object_or_404(Timetable, id=timetable_id)
    form = AddEvent()
    print("Form data:", request.POST)

    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    class_instances = ClassInstance.objects.filter(
        instance_date__range=(start_of_week, end_of_week)
    ).order_by('instance_date')

    if request.method == "POST":
        form = AddEvent(request.POST)
        if form.is_valid():
            class_type = form.cleaned_data['class_type']
            start_time = form.cleaned_data['start_time']
            finish_time = form.cleaned_data['finish_time']
            day_of_week = form.cleaned_data['day']
            repeat = form.cleaned_data.get('repeat', False)

            day_map = {
                'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3,
                'FRI': 4, 'SAT': 5, 'SUN': 6
            }

            today = timezone.now().date()
            target_weekday = day_map[day_of_week]
            days_ahead = (target_weekday - today.weekday() + 7) % 7

            if days_ahead == 0:
                days_ahead += 7

            next_date = today + timedelta(days=days_ahead)

            start_datetime = timezone.make_aware(
                datetime.combine(next_date, start_time)
            )
            finish_datetime = timezone.make_aware(
                datetime.combine(next_date, finish_time)
            )

            ClassInstance.objects.create(
                class_type=class_type,
                instance_date=next_date,
                start_time=start_datetime,
                finish_time=finish_datetime,
                day=day_of_week
            )

            if repeat:
                for _ in range(1, 4):
                    next_date += timedelta(weeks=1)
                    start_datetime = timezone.make_aware(
                        datetime.combine(next_date, start_time)
                    )
                    finish_datetime = timezone.make_aware(
                        datetime.combine(next_date, finish_time)
                    )

                    ClassInstance.objects.create(
                        class_type=class_type,
                        instance_date=next_date,
                        start_time=start_datetime,
                        finish_time=finish_datetime,
                        day=day_of_week
                    )

            return redirect('timetable_view',
                            timetable_id=timetable_instance.id)
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
    html_string = render_to_string(
        'booking_confirmation_pdf.html', {'booking': booking}
        )
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="booking_confirmation_{booking.id}.pdf"'
        )
    HTML(string=html_string).write_pdf(response)
    return response


@login_required
def account_details(request):
    if request.method == 'POST':
        if 'participant_id' in request.POST:
            participant_id = request.POST.get('participant_id')
            field_name = request.POST.get('field_name')
            value = request.POST.get(field_name)
            form = ParticipantForm(request.POST)
            print(
                 f"Updating participant: {participant_id}, "
                 f"Field: {field_name}, Value: {value}"
                 )

            if form.is_valid():
                try:
                    participant = Participant.objects.get(
                                id=participant_id,
                                user=request.user
                                )
                    setattr(participant, field, form.cleaned_data[field])
                    participant.save()
                    messages.success(request,
                                     "Participant updated successfully.")
                except Participant.DoesNotExist:
                    messages.error(request,
                                   "Participant does not exist.")
                except Exception as e:
                    messages.error(request,
                                   f"Error updating participant: {str(e)}")
                return redirect('account_details')
        else:
            form = UserEditForm(request.POST, instance=request.user)
            if form.is_valid():
                field_name = request.POST.get('field_name')
                if field_name in form.fields:
                    setattr(request.user, field_name,
                            form.cleaned_data[field_name])
                    request.user.save()
                return redirect('account_details')
    else:
        form = UserEditForm(instance=request.user)
        participants = request.user.participants.all()
        participant_forms = [ParticipantForm(instance=p)
                             for p in participants]
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
    form = ContactForm
    if request.method == 'POST':
        form = ContactForm(request.POST)
        return redirect('contact_success')
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