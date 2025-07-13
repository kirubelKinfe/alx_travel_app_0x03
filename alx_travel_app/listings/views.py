from django.shortcuts import render

from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Booking, Payment
from chapa import Chapa
from celery import shared_task
import uuid
from .tasks import send_booking_confirmation_email

class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows listings to be viewed or edited.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only for unauthenticated users

    def perform_create(self, serializer):
        # Automatically set the owner to the current user
        serializer.save(owner=self.request.user)

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only for unauthenticated users

    def perform_create(self, serializer):
        # Automatically set the user to the current user
        booking = serializer.save(user=self.request.user)
        send_booking_confirmation_email.delay(booking.id)





chapa = Chapa(settings.CHAPA_SECRET_KEY)

class InitiatePaymentView(APIView):
    def post(self, request):
        booking_id = request.data.get('booking_id')
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            tx_ref = f"TRAVEL-{uuid.uuid4()}"
            
            response = chapa.initialize(
                email=request.user.email,
                amount=booking.total_amount,
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                tx_ref=tx_ref,
                callback_url='http://localhost:8000/api/payments/verify/',
            )

            if response.get('status') == 'success':
                Payment.objects.create(
                    booking=booking,
                    user=request.user,
                    amount=booking.total_amount,
                    transaction_id=tx_ref,
                    status='PENDING'
                )
                return Response({
                    'message': 'Payment initiated successfully',
                    'checkout_url': response['data']['checkout_url']
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Failed to initiate payment'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Booking.DoesNotExist:
            return Response({
                'error': 'Booking not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyPaymentView(APIView):
    def get(self, request):
        tx_ref = request.GET.get('tx_ref')
        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
            verification_response = chapa.verify(tx_ref)
            
            if verification_response.get('status') == 'success':
                payment.status = 'COMPLETED'
                payment.save()
                send_confirmation_email.delay(request.user.email, payment.id)
                return Response({
                    'message': 'Payment verified successfully',
                    'status': payment.status
                }, status=status.HTTP_200_OK)
            else:
                payment.status = 'FAILED'
                payment.save()
                return Response({
                    'message': 'Payment verification failed',
                    'status': payment.status
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Payment.DoesNotExist:
            return Response({
                'error': 'Payment not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@shared_task
def send_confirmation_email(user_email, payment_id):
    payment = Payment.objects.get(id=payment_id)
    subject = 'Payment Confirmation'
    message = f'Thank you for your payment of {payment.amount}. Your booking is confirmed!'
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )