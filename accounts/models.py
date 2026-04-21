from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ROLE_CHOICES = (
        ('shipper', 'Shipper'),
        ('carrier', 'Carrier'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='shipper')
    company_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Company Name')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Phone Number')
    position = models.CharField(max_length=255, blank=True, null=True, verbose_name='Position')
    is_approved = models.BooleanField(default=True, verbose_name='Approved')
    
    # company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='Rating')
    total_reviews = models.PositiveIntegerField(default=0, verbose_name='Total Reviews')
    registration_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Registration Date',
    )
    last_active = models.DateTimeField(auto_now=True, verbose_name='Last Active')
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['is_approved']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_shipper(self):
        return self.role == 'shipper'
    
    @property
    def is_carrier(self):
        return self.role == 'carrier'

