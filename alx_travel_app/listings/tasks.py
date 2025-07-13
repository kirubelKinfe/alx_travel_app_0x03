from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking

@shared_task
def send_booking_confirmation_email(booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        subject = 'Booking Confirmation'
        message = f'Thank you for your booking, {booking.user.first_name}! Your booking for {booking.listing.title} is confirmed.'
        recipient_list = [booking.user.email]
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list,
            fail_silently=False,
        )
    except Booking.DoesNotExist:
        pass  # Optionally log this error 