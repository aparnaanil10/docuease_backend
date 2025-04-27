from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Hospital,Booking
from django.shortcuts import get_object_or_404

def hospital_list(request):
    if request.method== "GET":
        hospitals = list(Hospital.objects.values('id', 'name', 'location'))
        return JsonResponse(hospitals, safe=False)


@csrf_exempt
def create_booking(request):
    if request.method=='POST':
        data=json.loads(request.body)
        name=data.get('name')
        age=data.get('age')
        description=data.get('description')


        booking = Booking.objects.create(
            name=name,
            age=age,
            description=description
        )

        return JsonResponse({'message': 'Booking successful', 'booking_id': booking.id}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)
def booking_list(request):
    bookings = list(Booking.objects.values())  # Fetch all bookings
    return JsonResponse(bookings, safe=False)
