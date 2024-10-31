# appapi/serializers.py

from rest_framework import serializers
from .models import CustomUser, Service, Booking

from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number','rating','country','state','email', 'username', 'password', 'role']  # Include any other required fields

    def create(self, validated_data):
        user = User(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email=validated_data['email'],
            phone_number = validated_data['phone_number'],
            rating = validated_data['rating'],
            username=validated_data['username'],
            country=validated_data['country'],
            state=validated_data['state'],
            role=validated_data['role'],  # Ensure this field is handled if you have it in your User model
            is_active=False  # Ensure the user is active
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','phone_number','rating','email','country','state', 'username', 'password', 'role']  # Include any other required fields
        







class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    provider = serializers.HyperlinkedRelatedField(view_name="swiftapi:user-detail", queryset=CustomUser.objects.all())

    class Meta:
        model = Service
        fields = ["title","provider","description","price_per_hour","availability_status","created_at","updated_at"]


class BookingsSerializer(serializers.HyperlinkedModelSerializer):
    customer = serializers.HyperlinkedRelatedField(view_name="swiftapi:user-detail", queryset=CustomUser.objects.all())
    service = serializers.HyperlinkedRelatedField(view_name="swiftapi:service-detail", queryset=Service.objects.all())
    provider = serializers.HyperlinkedRelatedField(view_name="swiftapi:user-detail", queryset=CustomUser.objects.all())

    class Meta:
        model = Booking
        fields = ["customer","service","provider","status","scheduled_date","scheduled_time","total_cost","created_at","updated_at"]

    #Ensure that a booking can only be created for an existing service by a provider
    def validate(self, data):
        # Ensure the selected provider offers the selected service
        service = data.get("service")
        provider = data.get("provider")
        if service.provider != provider:
            raise serializers.ValidationError("The selected provider does not offer this service.")
        
        # Ensure the logged-in customer is creating the booking for themselves
        if data.get("customer") != self.context["request"].user:
            raise serializers.ValidationError("Customers can only create bookings for themselves.")
        
        return data