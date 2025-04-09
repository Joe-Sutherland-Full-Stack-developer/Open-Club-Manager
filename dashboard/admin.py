from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone
from admin_extra_buttons.api import ExtraButtonsMixin, link
from .models import (
    Participant, ClassType, Timetable, ClassInstance, Booking,
    Customization, StripeIntegration, ContactRequest
)
from django import forms
from .forms import ClassInstanceForm
from bootstrap_datepicker_plus.widgets import TimePickerInput


class ParticipantInline(admin.StackedInline):
    model = Participant
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = (ParticipantInline,)


# Unregister the default UserAdmin
admin.site.unregister(User)


# Register the new CustomUserAdmin
admin.site.register(User, CustomUserAdmin)


# Register your models here.
admin.site.register(Participant)
admin.site.register(ClassType)
admin.site.register(Customization)
admin.site.register(ContactRequest)


class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'participant', 'class_instance', 'paid_or_member',
        'created_on', 'updated_on', 'active'
    ]
    list_filter = ['paid_or_member', 'active', 'created_on', 'updated_on']
    search_fields = [
        'id', 'user__username', 'participant__first_name',
        'participant__last_name'
    ]
    readonly_fields = ['id', 'created_on', 'updated_on']
    fields = [
        'user', 'participant', 'class_instance', 'paid_or_member', 'active',
        'created_on', 'updated_on'
    ]
    actions = [
        'set_inactive', 'set_active', 'mark_as_paid', 'mark_as_not_paid'
    ]
    autocomplete_fields = ['user']

    def set_inactive(self, request, queryset):
        queryset.update(active=False, updated_on=timezone.now())
    set_inactive.short_description = (
        "Mark selected bookings as inactive. Use this to cancel bookings "
        "without deleting them"
    )

    def set_active(self, request, queryset):
        queryset.update(active=True, updated_on=timezone.now())
    set_active.short_description = "Mark selected bookings as active"

    def mark_as_paid(self, request, queryset):
        queryset.update(paid_or_member=True, updated_on=timezone.now())
    mark_as_paid.short_description = "Mark selected bookings as paid"

    def mark_as_not_paid(self, request, queryset):
        queryset.update(paid_or_member=False, updated_on=timezone.now())
    mark_as_not_paid.short_description = "Mark selected bookings as not paid"


admin.site.register(Booking, BookingAdmin)


# Custom Forms
class TimetableForm(forms.ModelForm):
    # Define the available choices for selection
    selected_days = forms.MultipleChoiceField(
        label=Timetable._meta.get_field("selected_days").verbose_name,
        choices=Timetable.day_choices,
        required=not Timetable._meta.get_field("selected_days").blank,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Timetable
        fields = ['name', 'active', 'selected_days',
                  'start_time', 'end_time', 'notes']
        widgets = {
            "start_time": TimePickerInput(options={
                    "format": "HH:mm",
                    "stepping": 15,
                    "showClose": True,
                    "showClear": True,
                }
            ),
            "end_time": TimePickerInput(options={
                    "format": "HH:mm",
                    "stepping": 15,
                    "showClose": True,
                    "showClear": True,
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['selected_days'].initial = self.instance.selected_days

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.selected_days = self.cleaned_data['selected_days']
        if commit:
            instance.save()
        return instance


@admin.register(Timetable)
class TimetableAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    form = TimetableForm
    list_display = ["__str__"]
    fields = ['name', 'active', 'selected_days',
              'start_time', 'end_time', 'notes']
    
    @link(label="Manage this Timetable", change_list=False, html_attrs={'style': 'background-color:#6CDC73;color:black'})
    def edit_timetable(self, button):
        # Extract timetable_id from the current request's URL
        timetable_id = button.context['request'].resolver_match.kwargs.get('object_id')

        # Generate the URL for the timetable editor
        url = reverse('timetable_view', kwargs={'timetable_id': timetable_id})

        # Set the button's href attribute to this URL
        button.href = url


@admin.register(ClassInstance)
class ClassInstAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'class_type', 'day', 'start_time', 'finish_time', 'capacity', 'instance_date')

    # Fields to search by
    search_fields = ('id', 'class_type__name', 'day', 'timetable__name')

    # Filters for the right-hand sidebar
    list_filter = ('class_type', 'day', 'instance_date', 'timetable')

    # Default ordering of the list view
    ordering = ('-instance_date', 'start_time')

    # Add ordering buttons to the columns
    list_display_links = ('id', 'class_type')  # Make the ID clickable to edit the instance

    form = ClassInstanceForm
    
    fields = ['class_type', 'instance_date', 'day',
              'start_time', 'finish_time', 'capacity',
              'attendees', 'timetable']


class StripeIntegrationForm(forms.ModelForm):
    class Meta:
        model = StripeIntegration
        fields = '__all__'  # Include all fields or specify them explicitly

    stripe_secret_key = forms.CharField(widget=forms.PasswordInput(),
                                        required=False)


@admin.register(StripeIntegration)
class StripeKeysAdmin(admin.ModelAdmin):
    list_display = ('masked_secret_key', 'stripe_publishable_key')
    form = StripeIntegrationForm  # Use the custom form

    def masked_secret_key(self, obj):
        return ('******************'
                '*******************')  # Return a masked string
    masked_secret_key.short_description = 'Secret Key'

    def changeform_view(self, request, object_id=None,
                        form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id,
                                       form_url, extra_context)
