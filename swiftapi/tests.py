from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import CustomUser, Service, Booking
# Create your tests here.
    


class UserRegistration(TestCase):
    def setUp(self):
        self.client = APIClient()  # This client helps us simulate requests in tests
        self.url = reverse('swiftapi:register')   # The URL for the registration endpoint

    def test_user_registration(self):
        data = {
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '1234567890',
        'country': 'Test Country',
        'state': 'Test State',
        'email': 'testuser@example.com',
        'username': 'testuser',
        'password': 'testpassword123',
        'role': 'customer',  # Assuming you have this role in your model
        'rating': 0.0  # Add a rating value here
        }
        response = self.client.post(self.url, data, format='json')  # Simulate a POST request
        self.assertEqual(response.status_code, 201)  # Check if we got a 'created' response
        self.assertIn('msg', response.data)  # Check if the response contains a success message


class ServiceListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.service_list_url = reverse('swiftapi:service-list')
        self.user = CustomUser.objects.create_user(
            username="provider1", password="password123", role="provider"
        )
        self.client.force_authenticate(user=self.user)  # Login as provider

    def test_service_list_caching(self):
        # Simulate a GET request to retrieve the list of services
        response = self.client.get(self.service_list_url)
        self.assertEqual(response.status_code, 200)  # Check that it returns 200 OK

        # Add a service and check if it doesn't show immediately due to caching
        Service.objects.create(
            provider=self.user,
            title="New Service",
            description="Test service",
            price_per_hour=50.00
        )

        # Check if the new service is not immediately visible (cached response)
        response_cached = self.client.get(self.service_list_url)
        self.assertNotIn("New Service", response_cached.json())