from django.urls import path
from .views import get_doctors_by_disease, get_doctor_availability, book_appointment,get_appointment_history,cancel_appointment,reschedule_appointment,case_sheet_view

urlpatterns = [
    path('recommend/', get_doctors_by_disease, name='doctor-recommendation'),
    path('availability/', get_doctor_availability, name='doctor-availability'),
    path('book/', book_appointment, name='book-appointment'),
    path('history/', get_appointment_history, name='appointment-history'),
    path('cancel/<int:appointment_id>/', cancel_appointment, name='cancel-appointment'),
    path('reschedule/<int:appointment_id>/', reschedule_appointment, name='reschedule-appointment'),
    path('case-sheet/<str:username>/', case_sheet_view, name='case-sheet'),
    
]
