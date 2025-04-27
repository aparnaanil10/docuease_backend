from django.urls import path
from .views import hospital_list,create_booking,booking_list

urlpatterns = [
    path('hospitals/', hospital_list, name='hospital-list'),
    path('booking/', create_booking,name='create_booking'),
    path('api/bookings/', booking_list, name='booking-list'),
]