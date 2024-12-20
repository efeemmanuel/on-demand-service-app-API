from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.


# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ['email', 'username', 'role', 'is_verified', 'is_active']
#     list_filter = ['is_verified', 'is_active', 'role']
#     ordering = ['email']


# admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(CustomUser)

admin.site.register(Service
admin.site.register(Booking)
