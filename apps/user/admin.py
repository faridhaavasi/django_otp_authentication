from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('mobile', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'is_verify')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'is_verify')
    fieldsets = (
        (None, {'fields': ('mobile', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verify', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')
        }),
    )
    search_fields = ('mobile', 'email')
    ordering = ('mobile',)

admin.site.register(CustomUser, CustomUserAdmin)
