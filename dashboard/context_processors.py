# context_processors.py
from .models import Customization, Timetable

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
    timetable_instances = Timetable.objects.all()  # Adjust this query as needed (e.g., filter by date)

    return {
        'timetables': timetable_instances,
    }
