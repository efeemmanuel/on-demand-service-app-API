# swiftapi/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS




class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow users to view and edit only their own profile.
    Admin users can view and edit any profile.
    """

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) for all authenticated users to view their profile
        if request.method in SAFE_METHODS:
            return obj == request.user or request.user.is_staff
        
        # For other actions, only the owner or admin users can perform them
        return obj == request.user or request.user.is_staff













class IsProviderOrReadOnly(BasePermission):
    """
    Custom permission to allow only providers to create, update, or delete services.
    Anyone can read (SAFE_METHODS).
    """

    def has_permission(self, request, view):
        # Allow read-only access for all users
        if request.method in SAFE_METHODS:
            return True
        # Only allow providers to create, update, or delete services
        return request.user.is_authenticated and request.user.role == "provider"

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for all users
        if request.method in SAFE_METHODS:
            return True
        # Allow access only if the user is the service owner or an admin
        return obj.provider == request.user or request.user.is_staff
    




class IsCustomerOrProviderOrAdmin(BasePermission):
    """
    Custom permission to allow:
    - Customers to create bookings and view/manage their bookings.
    - Providers to view/manage bookings related to their services.
    - Admins to view/manage all bookings.
    """

    def has_permission(self, request, view):
        # Allow booking creation only for authenticated users with a "customer" role
        if request.method == "POST":
            return request.user.is_superuser or request.user.role == "customer"
        # For non-creation requests, ensure the user is authenticated
        return request.user.is_superuser or request.user.role == "customer"

    def has_object_permission(self, request, view, obj):
        # Read-only access is allowed for all authenticated users to their relevant bookings
        if request.method in SAFE_METHODS:
            return (
                request.user == obj.customer  # The customer who made the booking
                or request.user == obj.provider  # The provider of the booked service
                or request.user.is_staff  # Admin access
            )
        # Write access is allowed only if:
        # - The user is the customer and is managing their booking
        # - The user is the provider of the service linked to the booking
        # - The user is an admin
        return (
            request.user == obj.customer
            or request.user == obj.provider
            or request.user.is_staff
        )
    



