from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'date_of_birth', 'is_staff']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        (_('Additional Info'), {'fields': ('date_of_birth', 'profile_photo')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Additional Info'), {'fields': ('date_of_birth', 'profile_photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
