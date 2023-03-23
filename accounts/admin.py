from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Define the fields to display in the list view
    list_display = ('username', 'email', 'name', 'is_staff')

    # Define the fields to edit in the detail view
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (('Personal Info'), {'fields': ('name', 'about', 'profile_picture')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Define the fields to filter by in the list view
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

admin.site.register(User, CustomUserAdmin)