<b>SwiftDemand API</b> <br>
SwiftDemand is a Django REST API built to power an on-demand service platform where customers can easily book services from professionals. This API focuses on seamless service booking functionality with robust authentication, authorization, and role-based access control.

Features <br>
User Management <br>
Custom User Model: Supports different roles—customers and providers—each with specific permissions and access.
User Registration: New users can register with relevant profile details, and providers can manage their offered services.
Authentication & Authorization
JWT Authentication: Secures API endpoints with JSON Web Token (JWT) for safe, session-free authentication.
Role-Based Permissions: Controls user access to endpoints depending on role (Customer, Provider, Admin).
Custom Permissions: Ensures users can only access their own data unless they have special permissions, like being an admin.
Service Management
Service Listings: Providers can create and manage services, while customers can view available services.
Caching: Service lists are cached to improve performance, avoiding frequent database hits for the same data.
Booking System
Booking Creation: Customers can book services from registered providers, while providers can manage bookings for their services.
Booking Validation: Ensures bookings match providers’ offered services and that customers can only book for themselves.
Booking Status Management: Bookings include status updates for better service tracking (Pending, Confirmed, Completed, Canceled).
Rate Limiting
Throttle Control: Limits the number of requests to endpoints, improving API security and preventing abuse.
