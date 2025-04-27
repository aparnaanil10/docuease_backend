import json
from datetime import date
from django.http import JsonResponse
from .serializers import CaseSheetSerializer
from rest_framework.response import Response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date, parse_time
from .models import Doctor, DiseaseSpecializationMapping, DoctorAvailability, Appointment
from rest_framework.decorators import api_view
User = get_user_model()

@require_GET
@csrf_exempt
def get_doctors_by_disease(request):
    disease = request.GET.get("disease", "").strip().lower()
    hospital_id = request.GET.get("hospital_id")  # 🆕 Get hospital filter

    if not hospital_id:
        return JsonResponse({"error": "Hospital ID required"}, status=400)

    try:
        mapping = DiseaseSpecializationMapping.objects.get(disease_name__iexact=disease)
    except DiseaseSpecializationMapping.DoesNotExist:
        return JsonResponse({"error": "No specialization found for this disease"}, status=400)

    doctors = Doctor.objects.filter(
        specialization__icontains=mapping.specialization,
        hospital__id=hospital_id  # 🆕 Filter doctors only in selected hospital
    )

    doctor_list = list(doctors.values("id", "name", "specialization", "hospital__name"))

    return JsonResponse({
        "predicted_disease": disease,
        "specialization": mapping.specialization,
        "doctors": doctor_list
    })

@require_GET
@csrf_exempt
def get_doctor_availability(request):
    doctor_id = request.GET.get("doctor_id")

    if not doctor_id:
        return JsonResponse({"error": "doctor_id is required"}, status=400)

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({"error": "Doctor not found"}, status=404)

    # Get all future availabilities
    from datetime import date
    availabilities = DoctorAvailability.objects.filter(
        doctor=doctor,
        date__gte=date.today()
    ).order_by("date", "time_slot")

    # Get all booked slots
    booked = Appointment.objects.filter(
        doctor=doctor,
        date__gte=date.today()
    ).values_list('date', 'time_slot')

    booked_set = {(b[0].isoformat(), b[1].strftime("%H:%M")) for b in booked}

    data = {}
    for slot in availabilities:
        d = slot.date.isoformat()
        t = slot.time_slot.strftime("%H:%M")
        status = 'booked' if (d, t) in booked_set else 'available'
        data.setdefault(d, []).append({'time': t, 'status': status})

    return JsonResponse({
        "doctor": doctor.name,
        "availability": data
    })

@require_POST
@csrf_exempt
def book_appointment(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        doctor_id = data.get("doctor_id")
        date_val = parse_date(data.get("date"))
        time_val = parse_time(data.get("time_slot"))

        if not all([username, doctor_id, date_val, time_val]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        try:
            user = User.objects.get(username=username)
            doctor = Doctor.objects.get(id=doctor_id)
        except (User.DoesNotExist, Doctor.DoesNotExist):
            return JsonResponse({"error": "Invalid user or doctor"}, status=404)

        already_booked = Appointment.objects.filter(
            doctor=doctor,
            date=date_val,
            time_slot=time_val
        ).exists()

        if already_booked:
            return JsonResponse({"error": "Selected slot already booked"}, status=400)

        Appointment.objects.create(
            user=user,
            doctor=doctor,
            date=date_val,
            time_slot=time_val
        )
       
        return JsonResponse({"message": "Appointment booked successfully!"}, status=201)
        

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
        
@require_GET
@csrf_exempt
def get_appointment_history(request):
    username = request.GET.get("username")
    if not username:
        return JsonResponse({"error": "Username required"}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    appointments = Appointment.objects.filter(user=user).order_by('-date', '-time_slot')
    history = [
        {
            "id":appt.id,
            "doctor": appt.doctor.name,
            "specialization": appt.doctor.specialization,
            "date": appt.date.strftime("%Y-%m-%d"),
            "time": appt.time_slot.strftime("%H:%M")
        }
        for appt in appointments
    ]
    return JsonResponse({"appointments": history})
@csrf_exempt
@require_http_methods(["DELETE"])
def cancel_appointment(request,appointment_id):
    try:
        

        appt = Appointment.objects.get(id=appointment_id)
        appt.status = 'cancelled'
        appt.save()
        
        return JsonResponse({"message": "Appointment cancelled successfully!"}, status=200)
        

    except Appointment.DoesNotExist:
        return JsonResponse({"error": "Appointment not found"}, status=404)
    
@csrf_exempt
@require_http_methods(["PUT"])
def reschedule_appointment(request, appointment_id):
    try:
        appt = Appointment.objects.get(id=appointment_id)
        data = json.loads(request.body)

        new_date = parse_date(data.get('new_date'))
        new_time = parse_time(data.get('new_time_slot'))

        if not new_date or not new_time:
            return JsonResponse({"error": "Date and time are required"}, status=400)

        # Check if the new slot is already booked
        if Appointment.objects.filter(doctor=appt.doctor, date=new_date, time_slot=new_time).exclude(id=appt.id).exists():
            return JsonResponse({"error": "Time slot already booked"}, status=400)

        # Update appointment
        appt.date = new_date
        appt.time_slot = new_time
        appt.status = 'rescheduled'
        appt.save()

        return JsonResponse({"message": "Appointment rescheduled"})
        
    except Appointment.DoesNotExist:
        return JsonResponse({"error": "Appointment not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def case_sheet_view(request, username):
    try:
        user = User.objects.get(username=username)
        appointments = Appointment.objects.filter(user=user).exclude(status='cancelled')
        serializer = CaseSheetSerializer(appointments, many=True)
        return Response({'case_sheet': serializer.data})
    except User.DoesNotExist:
        return Response({'case_sheet': []})

