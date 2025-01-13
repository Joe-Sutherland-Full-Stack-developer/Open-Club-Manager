"""
URL configuration for OpenClubManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('', dashboard_views.home, name='home'),
    path('login/', dashboard_views.CustomLoginView.as_view(), name='login'),
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    # path('dashboard/new_participant', dashboard_views.create_participant, name="create_participant"),
    path('timetable/<int:timetable_id>/', dashboard_views.timetable_view, name='timetable_view'),
    path('load-booking-form/<int:event_id>/', dashboard_views.load_booking_form, name='load_booking_form'),
    path('create-booking/', dashboard_views.create_booking, name='create_booking'),
    path('booking-confirmation/<int:booking_id>/', dashboard_views.booking_confirmation, name='booking_confirmation'),
    path('view-bookings/', dashboard_views.view_bookings, name='view_bookings'),
    path('booking-confirmation/pdf/<int:booking_id>/', dashboard_views.booking_confirmation_pdf, name='booking_confirmation_pdf'),
    path('account/', dashboard_views.account_details, name='account_details'),
    path('create-participant/', dashboard_views.create_participant, name='create_participant'),
    path('delete-participant/<int:participant_id>/', dashboard_views.delete_participant, name='delete_participant'),
    path('create-checkout-session/', dashboard_views.create_checkout_session, name='create-checkout-session'),
    path('contact/', dashboard_views.contact, name='contact'),
    
]

admin.site.site_header = "Open Club Manager"
admin.site.site_title = "Open Club Manager"
admin.site.index_title = "Welcome to Your admin portal"