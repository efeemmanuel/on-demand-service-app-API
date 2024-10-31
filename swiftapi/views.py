from rest_framework import viewsets, filters
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import  IsOwnerOrAdmin, IsProviderOrReadOnly, IsCustomerOrProviderOrAdmin
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"msg": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    permission_classes = [AllowAny] 




class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin] 
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(username=self.request.user.username)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsProviderOrReadOnly]  # Protect this view
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingsSerializer
    permission_classes = [IsAuthenticated, IsCustomerOrProviderOrAdmin]  # Protect this view
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    # Restrict customers from creating bookings for other customers.
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Booking.objects.all()
        elif user.role == "customer":
            return Booking.objects.filter(customer=user)
        elif user.role == "provider":
            return Booking.objects.filter(provider=user)
        return Booking.objects.none()

    def perform_create(self, serializer):
        # Automatically set the booking customer as the logged-in user
        serializer.save(customer=self.request.user)

