from django.shortcuts import render, get_object_or_404, redirect
from doctors.models import Doctor
from hospital.models import Hospital
from users.models import CustomUser
from doctors.models import Appointment

# Dashboard Home View
def dashboard_view(request):
    doctors = Doctor.objects.all()
    hospitals = Hospital.objects.all()
    users = CustomUser.objects.all()
    appointments = Appointment.objects.all()
    context = {
        'doctors': doctors,
        'hospitals': hospitals,
        'users': users,
        'appointments': appointments,
    }
    return render(request, 'admin_dashboard/dashboard.html', context)


# --------------- Doctor Management ------------------

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin_dashboard/doctor_list.html', {'doctors': doctors})

def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'admin_dashboard/doctor_detail.html', {'doctor': doctor})

def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.delete()
    return redirect('doctor_list')


# --------------- Hospital Management ------------------

def hospital_list(request):
    hospitals = Hospital.objects.all()
    return render(request, 'admin_dashboard/hospital_list.html', {'hospitals': hospitals})

def hospital_detail(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    return render(request, 'admin_dashboard/hospital_detail.html', {'hospital': hospital})

def hospital_delete(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    hospital.delete()
    return redirect('hospital_list')


# --------------- User Management ------------------

def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'admin_dashboard/user_list.html', {'users': users})

def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'admin_dashboard/user_detail.html', {'user': user})

def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.delete()
    return redirect('user_list')


# --------------- Booking / Appointment Management ------------------

def booking_list(request):
    bookings = Appointment.objects.all()
    return render(request, 'admin_dashboard/booking_list.html', {'bookings': bookings})

def booking_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'admin_dashboard/booking_detail.html', {'appointment': appointment})

def booking_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    return redirect('booking_list')
