from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.utils import timezone

from .models import User


# Unregister standard models

# First unregister standard User if it's already registered
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass  # Ignore error if model is not registered yet


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Display in list view
    list_display = (
        'username', 
        'email', 
        'get_role_badge', 
        'company_name', 
        'phone',
        'rating_stars',
        'is_active',
        'registration_date'
    )
    
    list_filter = (
        'role', 
        'is_approved', 
        'is_active', 
        'is_staff', 
        'is_superuser',
        'registration_date'
    )
    
    search_fields = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'company_name', 
        'phone'
    )
    
    readonly_fields = (
        'registration_date', 
        'last_active', 
        'rating', 
        'total_reviews',
        'display_avatar'
    )
    
    fieldsets = (
        ('Account Information', {
            'fields': (
                'username', 
                'email', 
                'password', 
                'role',
                'is_approved'
            )
        }),
        ('Personal Information', {
            'fields': (
                'first_name', 
                'last_name', 
                'company_name', 
                'position',
                'phone', 
                'website', 
                'address'
            )
        }),
        ('Ratings & Statistics', {
            'fields': (
                'rating', 
                'total_reviews',
                'display_avatar',
                'registration_date', 
                'last_active'
            ),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser',
                'groups', 
                'user_permissions'
            ),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 
                'email', 
                'password1', 
                'password2', 
                'role',
                'company_name',
                'phone'
            ),
        }),
    )
    
    actions = ['approve_users', 'disapprove_users', 'make_shipper', 'make_carrier']
    
    def get_role_badge(self, obj):
        colors = {
            'shipper': 'blue',
            'carrier': 'green',
            'admin': 'red',
        }
        color = colors.get(obj.role, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_role_display()
        )
    get_role_badge.short_description = 'Role'
    get_role_badge.admin_order_field = 'role'
       
    def rating_stars(self, obj):
        if obj.rating == 0:
            return 'No ratings'
        
        full_stars = int(obj.rating)
        half_star = 1 if obj.rating - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        
        stars = '★' * full_stars
        stars += '½' * half_star
        stars += '☆' * empty_stars
        
        return format_html(
            '<span style="color: #ffc107; font-size: 14px;">{} ({:.1f})</span>',
            stars,
            obj.rating
        )
    rating_stars.short_description = 'Rating'
    rating_stars.admin_order_field = 'rating'
    
    def display_avatar(self, obj):
        return format_html(
            '<div style="width: 50px; height: 50px; background: #007bff; '
            'border-radius: 50%; display: flex; align-items: center; '
            'justify-content: center; color: white; font-size: 20px; font-weight: bold;">'
            '{}</div>',
            obj.username[0].upper()
        )
    display_avatar.short_description = 'Avatar'
    
    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} users approved.')
    approve_users.short_description = 'Approve selected users'
    
    def disapprove_users(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} users disapproved.')
    disapprove_users.short_description = 'Disapprove selected users'
    
    def make_shipper(self, request, queryset):
        queryset.update(role='shipper')
        self.message_user(request, f'{queryset.count()} users changed to Shipper.')
    make_shipper.short_description = 'Change role to Shipper'
    
    def make_carrier(self, request, queryset):
        queryset.update(role='carrier')
        self.message_user(request, f'{queryset.count()} users changed to Carrier.')
    make_carrier.short_description = 'Change role to Carrier'
    
    def save_model(self, request, obj, form, change):
        if not change:  # New user
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


# Register Group back
@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    pass