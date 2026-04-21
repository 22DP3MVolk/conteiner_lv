from django.db import models
from django.conf import settings
from django.utils import timezone


class CargoStatus(models.Model):
    """Status options for cargo listings"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Status Name')
    code = models.CharField(max_length=20, unique=True, verbose_name='Status Code')
    color = models.CharField(max_length=20, default='gray', verbose_name='Color')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    order = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    
    class Meta:
        verbose_name = 'Cargo Status'
        verbose_name_plural = 'Cargo Statuses'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class CargoType(models.Model):
    """Type options for cargo"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Type Name')
    code = models.CharField(max_length=20, unique=True, verbose_name='Type Code')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='Icon')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    order = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    
    class Meta:
        verbose_name = 'Cargo Type'
        verbose_name_plural = 'Cargo Types'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class TransportStatus(models.Model):
    """Status options for transport listings"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Status Name')
    code = models.CharField(max_length=20, unique=True, verbose_name='Status Code')
    color = models.CharField(max_length=20, default='gray', verbose_name='Color')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    order = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    
    class Meta:
        verbose_name = 'Transport Status'
        verbose_name_plural = 'Transport Statuses'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class TransportType(models.Model):
    """Type options for transport"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Type Name')
    code = models.CharField(max_length=20, unique=True, verbose_name='Type Code')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='Icon')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    order = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    
    class Meta:
        verbose_name = 'Transport Type'
        verbose_name_plural = 'Transport Types'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Cargo(models.Model):
    shipper = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cargoes'
    )
    
    title = models.CharField(max_length=200, verbose_name='Load Title')
    description = models.TextField(blank=True, verbose_name='Description')
    
    pickup_city = models.CharField(max_length=100, verbose_name='Pickup City')
    pickup_address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Pickup Address')
    delivery_city = models.CharField(max_length=100, verbose_name='Delivery City')
    delivery_address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Delivery Address')
    
    pickup_date = models.DateField(verbose_name='Pickup Date')
    pickup_time = models.TimeField(blank=True, null=True, verbose_name='Pickup Time')
    delivery_date = models.DateField(blank=True, null=True, verbose_name='Delivery Date')
    delivery_time = models.TimeField(blank=True, null=True, verbose_name='Delivery Time')
    
    weight = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Weight (tons)')
    volume = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Volume (m³)')
    
    # Foreign keys to dynamic choices
    cargo_type = models.ForeignKey(
        CargoType,
        on_delete=models.PROTECT,
        related_name='cargoes',
        verbose_name='Cargo Type'
    )
    status = models.ForeignKey(
        CargoStatus,
        on_delete=models.PROTECT,
        related_name='cargoes',
        default=1,  # You'll need to set the actual default ID after initial migration
        verbose_name='Status'
    )
    
    length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name='Length (m)')
    width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name='Width (m)')
    height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name='Height (m)')
    
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Offered Price')
    price_negotiable = models.BooleanField(default=True, verbose_name='Price Negotiable')
    
    views_count = models.PositiveIntegerField(default=0, verbose_name='Views')
    contact_count = models.PositiveIntegerField(default=0, verbose_name='Contacts Received')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateField(blank=True, null=True, verbose_name='Expires At')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargoes'
        indexes = [
            models.Index(fields=['pickup_city', 'delivery_city']),
            models.Index(fields=['pickup_date']),
            models.Index(fields=['status']),
            models.Index(fields=['cargo_type']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.pickup_city} → {self.delivery_city}"
    
    @property
    def is_active(self):
        return self.status.code == 'open' and (not self.expires_at or self.expires_at >= timezone.now().date())


class Transport(models.Model):
    carrier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transports'
    )
    
    title = models.CharField(max_length=200, verbose_name='Vehicle Title')
    description = models.TextField(blank=True, verbose_name='Description')
    
    available_city_from = models.CharField(max_length=100, verbose_name='Available From City')
    available_city_to = models.CharField(max_length=100, blank=True, null=True, verbose_name='Available To City')
    current_location = models.CharField(max_length=100, blank=True, null=True, verbose_name='Current Location')
    
    available_from_date = models.DateField(verbose_name='Available From Date')
    available_from_time = models.TimeField(blank=True, null=True, verbose_name='Available From Time')
    available_to_date = models.DateField(blank=True, null=True, verbose_name='Available To Date')
    available_to_time = models.TimeField(blank=True, null=True, verbose_name='Available To Time')
    
    # Foreign keys to dynamic choices
    transport_type = models.ForeignKey(
        TransportType,
        on_delete=models.PROTECT,
        related_name='transports',
        verbose_name='Vehicle Type'
    )
    status = models.ForeignKey(
        TransportStatus,
        on_delete=models.PROTECT,
        related_name='transports',
        default=1,  # You'll need to set the actual default ID after initial migration
        verbose_name='Status'
    )
    
    capacity_weight = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Capacity (tons)')
    capacity_volume = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Capacity (m³)')
    
    truck_model = models.CharField(max_length=100, blank=True, null=True, verbose_name='Truck Model')
    year = models.PositiveIntegerField(blank=True, null=True, verbose_name='Year')
    license_plate = models.CharField(max_length=20, blank=True, null=True, verbose_name='License Plate')
    
    price_per_km = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Price per km')
    fixed_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Fixed Price')
    price_negotiable = models.BooleanField(default=True, verbose_name='Price Negotiable')
    
    has_gps = models.BooleanField(default=False, verbose_name='GPS Tracking')
    has_driver = models.BooleanField(default=True, verbose_name='Driver Included')
    has_temperature_control = models.BooleanField(default=False, verbose_name='Temperature Control')
    insurance_included = models.BooleanField(default=False, verbose_name='Insurance Included')
    
    views_count = models.PositiveIntegerField(default=0, verbose_name='Views')
    contact_count = models.PositiveIntegerField(default=0, verbose_name='Contacts Received')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateField(blank=True, null=True, verbose_name='Expires At')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Transport'
        verbose_name_plural = 'Transport'
        indexes = [
            models.Index(fields=['available_city_from']),
            models.Index(fields=['available_from_date']),
            models.Index(fields=['status']),
            models.Index(fields=['transport_type']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.transport_type.name} ({self.capacity_weight}t)"
    
    @property
    def is_available(self):
        return self.status.code == 'available' and (not self.expires_at or self.expires_at >= timezone.now().date())


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='messages'
    )
    transport = models.ForeignKey(
        Transport,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='messages'
    )
    
    subject = models.CharField(max_length=200, blank=True, verbose_name='Subject')
    content = models.TextField(verbose_name='Message Content')
    is_read = models.BooleanField(default=False, verbose_name='Is Read')
    read_at = models.DateTimeField(blank=True, null=True, verbose_name='Read At')
    
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='replies'
    )
    is_deleted_by_sender = models.BooleanField(default=False)
    is_deleted_by_receiver = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        indexes = [
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class ListingReport(models.Model):
    REPORT_REASONS = [
        ('spam', 'Spam'),
        ('fraud', 'Fraud / Scam'),
        ('inappropriate', 'Inappropriate Content'),
        ('duplicate', 'Duplicate Listing'),
        ('expired', 'Expired'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    
    LISTING_TYPES = [
        ('cargo', 'Cargo'),
        ('transport', 'Transport'),
    ]
    
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES)
    listing_id = models.PositiveIntegerField()
    
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='resolved_reports'
    )
    
    resolved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Listing Report'
        verbose_name_plural = 'Listing Reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report on {self.listing_type} #{self.listing_id} - {self.reason}"