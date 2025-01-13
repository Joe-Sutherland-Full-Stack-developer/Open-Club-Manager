from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings
from bootstrap_datepicker_plus.widgets import DatePickerInput
from datetime import timedelta, datetime
from colorfield.fields import ColorField
from cloudinary.models import CloudinaryField
# from encrypted_model_fields.fields import EncryptedCharField


class ClassType(models.Model):
    duration_choices = (
        (15, '15 Minutes'), (30, '30 Minutes'),
        (45, '45 Minutes'), (60, '1 Hour'),
        (75, '1 Hour 15 Minutes'),
        (90, '1 Hour 30 Minutes'),
        (105, '1 hour 45 Minutes'),
        (120, '2 Hours'),
        (135, '2 Hours 15 Minutes'),
        (150, '2 Hours 30 Minutes'),
        (165, '2 Hours 45 Minutes'),
        (180, '3 Hours'),
        (195, '3 Hours 15 Minutes'),
        (210, '3 Hours 30 Minutes'),
        (225, '3 Hours 45 Minutes'),
        (240, '4 Hours'),
        (255, '4 Hours 15 Minutes'),
        (270, '4 Hours 30 Minutes'),
        (285, '4 Hours 45 Minutes'),
        (300, '5 Hours')
    )
    name = models.CharField(max_length=100)
    age_group_min = models.IntegerField()
    age_group_max = models.IntegerField(default=99)
    duration = models.IntegerField(choices=duration_choices)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    default_capacity = models.IntegerField(default=0)
    color_value = ColorField(default='#FF0000')

    def __str__(self):
        return self.name


class Timetable(models.Model):
    day_choices = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    selected_days = models.JSONField(
        verbose_name="Timetabled days",
        blank=True,
        null=True,
        help_text=("Store selected days of the week "
                   "as a JSON array (e.g., ['MON', 'TUE'])")
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @property
    def time_slots(self):
        """Generate 15-minute time slots between start_time and end_time."""
        start_datetime = datetime.combine(datetime.today(), self.start_time)
        end_datetime = datetime.combine(datetime.today(), self.end_time)

        slots = []

        current_time = start_datetime
        while current_time <= end_datetime:
            slots.append(current_time.strftime('%H:%M'))
            current_time += timedelta(minutes=15)

        return slots


class ClassInstance(models.Model):
    class_type = models.ForeignKey('ClassType', on_delete=models.CASCADE)
    instance_date = models.DateField()
    day = models.CharField(
        max_length=3,
        choices=[
            ('MON', 'Monday'),
            ('TUE', 'Tuesday'),
            ('WED', 'Wednesday'),
            ('THU', 'Thursday'),
            ('FRI', 'Friday'),
            ('SAT', 'Saturday'),
            ('SUN', 'Sunday'),
        ]
    )
    start_time = models.TimeField()
    finish_time = models.TimeField()
    capacity = models.IntegerField(default=0)
    attendees = models.ManyToManyField('Booking')

    def __str__(self):
        return (
            f"{self.class_type} | {self.start_time.strftime('%H:%M')} | "
            f"{self.instance_date.strftime('%A %d %B')}"
        )


class Booking(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE)
    class_instance = models.ForeignKey('ClassInstance', on_delete=models.CASCADE)
    paid_or_member = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            max_id = Booking.objects.all().aggregate(models.Max('id'))['id__max']
            self.id = 100000 if max_id is None else max_id + 1
            if self.id > 999999:
                raise ValidationError("Maximum ID limit reached")
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class Participant(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='participants'
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    is_member = models.BooleanField(default=False)
    address = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_number = models.CharField(max_length=15)
    additional_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Customization(models.Model):
    business_name = models.CharField(max_length=200, default='Open Club Manager')
    currency_symbol = models.CharField(max_length=5, default='£')
    brand_color_1 = ColorField(default='#AECBEB', blank=True)
    brand_color_2 = ColorField(default='#71A5DE', blank=True)
    brand_color_3 = ColorField(default='#0353A4', blank=True)
    brand_color_white = ColorField(default='#f8f9fb', blank=True)
    brand_color_dark = ColorField(default='#061A40', blank=True)
    confirmation_message = models.CharField(
        max_length=200, default='See you soon!'
    )
    default_country = models.CharField(
        max_length=200, default='United Kingdom'
    )
    default_language = models.CharField(max_length=200, default='English')
    logo = CloudinaryField('image', null=True, blank=True)
    favicon = CloudinaryField('image', null=True, blank=True)
    custom_font = models.CharField(max_length=200, default='Arial')
    site_title = models.CharField(
        max_length=200, default="Open Club Manager"
    )
    site_tagline = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_other = models.CharField(max_length=20, blank=True)
    contact_address_1 = models.CharField(max_length=200, blank=True)
    contact_address_2 = models.CharField(max_length=200, blank=True)
    contact_address_city = models.CharField(max_length=200, blank=True)
    contact_address_state = models.CharField(max_length=200, blank=True)
    contact_address_zip = models.CharField(max_length=200, blank=True)
    # Enable the following fields once Email integration is set up
    # smtp_server = models.CharField(max_length=255, blank=True)
    # smtp_port = models.IntegerField(default=587)
    # smtp_username = models.CharField(max_length=255, blank=True)
    # smtp_password = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "Customization Settings"

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

    def save(self, *args, **kwargs):
        if not self.pk and Customization.objects.exists():
            raise ValidationError(
                "Only one instance of Customization is allowed. "
                "Please edit the existing instance instead"
            )
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    contact_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username}"


class ContactRequest(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


class StripeIntegration(models.Model):
    currency_choices = [
        ('AUD', 'Australian Dollar'),
        ('BGN', 'Bulgarian Lev'),
        ('CAD', 'Canadian Dollar'),
        ('CHF', 'Swiss Franc'),
        ('CZK', 'Czech Koruna'),
        ('DKK', 'Danish Krone'),
        ('EUR', 'Euro'),
        ('gbp', 'British Pound'),
        ('HKD', 'Hong Kong Dollar'),
        ('JPY', 'Japanese Yen'),
        ('MXN', 'Mexican Peso'),
        ('NOK', 'Norwegian Krone'),
        ('NZD', 'New Zealand Dollar'),
        ('PLN', 'Polish Złoty'),
        ('RON', 'Romanian Leu'),
        ('SEK', 'Swedish Krona'),
        ('SGD', 'Singapore Dollar'),
        ('USD', 'United States Dollar'),
    ]

    stripe_secret_key = models.CharField(max_length=200, blank=True)
    stripe_publishable_key = models.CharField(max_length=200, blank=True)
    currency = models.CharField(
        max_length=3, choices=currency_choices, default='GBP'
    )

    def __str__(self):
        return "Stripe integration settings"

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

    def save(self, *args, **kwargs):
        if not self.pk and StripeIntegration.objects.exists():
            raise ValidationError(
                "Only one instance of Stripe integration is allowed. "
                "Please edit the existing instance instead."
            )
        super().save(*args, **kwargs)
