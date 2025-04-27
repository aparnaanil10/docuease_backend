from django.core.management.base import BaseCommand
from doctors.models import Doctor, DoctorAvailability
from datetime import date, timedelta, datetime, time

class Command(BaseCommand):
    help = 'Generate availability slots for doctors'

    def add_arguments(self, parser):
        parser.add_argument('--interval', type=int, default=60, help='Slot duration in minutes')
        parser.add_argument('--days', type=int, default=7, help='How many days to generate from today')
        parser.add_argument('--start_hour', type=int, default=9, help='Working start hour')
        parser.add_argument('--end_hour', type=int, default=17, help='Working end hour')
        parser.add_argument('--include_weekends', action='store_true', help='Include Saturday & Sunday')
        parser.add_argument('--doctor_ids', nargs='+', type=int, help='Doctor IDs to generate slots for')

    def handle(self, *args, **options):
        interval = options['interval']
        num_days = options['days']
        include_weekends = options['include_weekends']
        start_hour = options['start_hour']
        end_hour = options['end_hour']
        doctor_ids = options['doctor_ids']

        # Choose doctors
        if doctor_ids:
            doctors = Doctor.objects.filter(id__in=doctor_ids)
        else:
            doctors = Doctor.objects.all()

        created = 0
        today = date.today()

        for doctor in doctors:
            for day_offset in range(num_days):
                slot_date = today + timedelta(days=day_offset)

                # Skip weekends if not included
                if not include_weekends and slot_date.weekday() >= 5:
                    continue

                # Time range: 9:00 to 17:00 (or what user chooses)
                current_time = datetime.combine(slot_date, time(hour=start_hour))
                end_time = datetime.combine(slot_date, time(hour=end_hour))

                while current_time < end_time:
                    slot_time = current_time.time()

                    # Create or ignore if already exists
                    obj, created_flag = DoctorAvailability.objects.get_or_create(
                        doctor=doctor,
                        date=slot_date,
                        time_slot=slot_time
                    )
                    if created_flag:
                        created += 1

                    current_time += timedelta(minutes=interval)

        self.stdout.write(self.style.SUCCESS(f" {created} slots created!"))
