from rest_framework import serializers
from .models import DoctorAvailability, Appointment, Doctor
from rest_framework import serializers
from .models import Appointment
class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class CaseSheetSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()
    hospital = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    date = serializers.DateField(format="%Y-%m-%d")
    time = serializers.TimeField(source='time_slot', format="%H:%M")

    class Meta:
        model = Appointment
        fields = ['doctor', 'hospital', 'patient_name', 'age', 'date', 'time', 'status']

    def get_doctor(self, obj):
        if obj.doctor:
            return obj.doctor.name
        return "Unknown Doctor"

    def get_hospital(self, obj):
        if obj.doctor and obj.doctor.hospital:
            return obj.doctor.hospital.name
        return "Unknown Hospital"

    def get_patient_name(self, obj):
        if obj.user:
            return obj.user.full_name
        return "Unknown Patient"

    def get_age(self, obj):
        if obj.user and hasattr(obj.user, 'age') and obj.user.age is not None:
            return obj.user.age
        return "N/A"
