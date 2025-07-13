from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet
from listings.views import InitiatePaymentView, VerifyPaymentView


# Create a router and register viewsets
router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')

# Define URL patterns
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/payments/initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('api/payments/verify/', VerifyPaymentView.as_view(), name='verify-payment'),
]