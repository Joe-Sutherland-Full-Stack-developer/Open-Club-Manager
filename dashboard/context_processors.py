# context_processors.py
from .models import Customization, Timetable, StripeIntegration


def customization_settings(request):
    try:
        customization = Customization.get_solo()  # Get the singleton instance
    except Customization.DoesNotExist:
        customization = None  # Handle case where no customization exists

    return {
        'customization': customization
    }


def timetables(request):
    # Retrieve all timetable instances
    timetable_instances = Timetable.objects.all()

    return {
        'timetables': timetable_instances,
    }


def stripe_context(request):
    stripe_instance = StripeIntegration.objects.first()
    return {'stripe_instance': stripe_instance}
