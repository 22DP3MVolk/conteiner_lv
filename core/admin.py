from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone

from .models import (
    Cargo, Transport, Message, ListingReport,
    CargoStatus, CargoType, TransportStatus, TransportType
)


@admin.register(CargoStatus)
class CargoStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'color_display', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    list_editable = ('order', 'is_active')
    
    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 12px;">{}</span>',
            obj.color,
            obj.name
        )
    color_display.short_description = 'Color'


@admin.register(CargoType)
class CargoTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'icon_display', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    list_editable = ('order', 'is_active')
    
    def icon_display(self, obj):
        return f"{obj.icon or '📦'} {obj.name}"
    icon_display.short_description = 'Type'


@admin.register(TransportStatus)
class TransportStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'color_display', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    list_editable = ('order', 'is_active')
    
    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 12px;">{}</span>',
            obj.color,
            obj.name
        )
    color_display.short_description = 'Color'


@admin.register(TransportType)
class TransportTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'icon_display', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    list_editable = ('order', 'is_active')
    
    def icon_display(self, obj):
        return f"{obj.icon or '🚛'} {obj.name}"
    icon_display.short_description = 'Type'


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'shipper_info',
        'route',
        'pickup_date',
        'weight',
        'cargo_type',
        'price_display',
        'status_display',
        'views_count'
    )
    
    list_filter = (
        'status',
        'cargo_type',
        'pickup_date',
        'created_at',
    )
    
    search_fields = (
        'title',
        'description',
        'pickup_city',
        'delivery_city',
        'shipper__username',
        'shipper__company_name',
        'shipper__email'
    )
    
    readonly_fields = (
        'views_count', 
        'contact_count', 
        'created_at', 
        'updated_at'
    )
    
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    def shipper_info(self, obj):
        return format_html(
            '{}<br><small>{}</small>',
            obj.shipper.company_name or obj.shipper.username,
            obj.shipper.email
        )
    shipper_info.short_description = 'Shipper'
    
    def route(self, obj):
        return f"{obj.pickup_city} → {obj.delivery_city}"
    route.short_description = 'Route'
    
    def price_display(self, obj):
        if obj.price:
            price_text = f"${obj.price:,.2f}"
            if obj.price_negotiable:
                return f"{price_text} (negotiable)"
            return price_text
        return 'Not specified'
    price_display.short_description = 'Price'
    
    def status_display(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 15px; font-size: 11px;">{}</span>',
            obj.status.color,
            obj.status.name
        )
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status__name'


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'carrier_info',
        'location',
        'available_from_date',
        'transport_type',
        'capacity_weight',
        'price_info',
        'status_display',
        'views_count'
    )
    
    list_filter = (
        'status',
        'transport_type',
        'available_from_date',
        'created_at',
    )
    
    search_fields = (
        'title',
        'description',
        'available_city_from',
        'available_city_to',
        'carrier__username',
        'carrier__company_name',
        'license_plate'
    )
    
    readonly_fields = (
        'views_count', 
        'contact_count', 
        'created_at', 
        'updated_at'
    )
    
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    def carrier_info(self, obj):
        return format_html(
            '{}<br><small>{}</small>',
            obj.carrier.company_name or obj.carrier.username,
            obj.carrier.email
        )
    carrier_info.short_description = 'Carrier'
    
    def location(self, obj):
        if obj.available_city_to:
            return f"{obj.available_city_from} → {obj.available_city_to}"
        return obj.available_city_from
    location.short_description = 'Location'
    
    def price_info(self, obj):
        if obj.price_per_km:
            price = f"${obj.price_per_km}/km"
        elif obj.fixed_price:
            price = f"${obj.fixed_price:,.2f}"
        else:
            price = 'Not specified'
        
        if obj.price_negotiable and (obj.price_per_km or obj.fixed_price):
            return f"{price} (negotiable)"
        return price
    price_info.short_description = 'Price'
    
    def status_display(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 15px; font-size: 11px;">{}</span>',
            obj.status.color,
            obj.status.name
        )
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status__name'




# @admin.register(Cargo)
# class CargoAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'title',
#         'shipper_info',
#         'route',
#         'pickup_date',
#         'weight',
#         'cargo_type',
#         'price_display',
#         'status',
#         'views_count'
#     )
    
#     list_filter = (
#         'status',
#         'cargo_type',
#         'pickup_date',
#         'created_at',
#     )
    
#     search_fields = (
#         'title',
#         'description',
#         'pickup_city',
#         'delivery_city',
#         'shipper__username',
#         'shipper__company_name',
#         'shipper__email'
#     )
    
#     readonly_fields = (
#         'views_count', 
#         'contact_count', 
#         'created_at', 
#         'updated_at'
#     )
    
#     list_per_page = 25
#     date_hierarchy = 'created_at'
    
#     fieldsets = (
#         ('Basic Information', {
#             'fields': (
#                 'shipper',
#                 'title',
#                 'description',
#                 'status'
#             )
#         }),
#         ('Route & Schedule', {
#             'fields': (
#                 'pickup_city',
#                 'pickup_address',
#                 'delivery_city',
#                 'delivery_address',
#                 'pickup_date',
#                 'pickup_time',
#                 'delivery_date',
#                 'delivery_time',
#             )
#         }),
#         ('Cargo Details', {
#             'fields': (
#                 'cargo_type',
#                 'weight',
#                 'volume',
#                 'length',
#                 'width',
#                 'height',
#                 'price',
#                 'price_negotiable',
#             )
#         }),
#         ('Statistics', {
#             'fields': (
#                 'views_count',
#                 'contact_count',
#                 'created_at',
#                 'updated_at',
#                 'expires_at'
#             ),
#             'classes': ('collapse',)
#         }),
#     )
    
#     actions = ['mark_as_open', 'mark_as_reserved', 'mark_as_closed']
    
#     def shipper_info(self, obj):
#         return format_html(
#             '{}<br><small>{}</small>',
#             obj.shipper.company_name or obj.shipper.username,
#             obj.shipper.email
#         )
#     shipper_info.short_description = 'Shipper'
#     shipper_info.admin_order_field = 'shipper__username'
    
#     def route(self, obj):
#         return f"{obj.pickup_city} → {obj.delivery_city}"
#     route.short_description = 'Route'
    
#     def price_display(self, obj):
#         if obj.price:
#             price_text = f"${obj.price:,.2f}"
#             if obj.price_negotiable:
#                 return f"{price_text} (negotiable)"
#             return price_text
#         return 'Not specified'
#     price_display.short_description = 'Price'
    
#     def mark_as_open(self, request, queryset):
#         queryset.update(status='open')
#         self.message_user(request, f'{queryset.count()} cargoes marked as open.')
#     mark_as_open.short_description = 'Mark as Open'
    
#     def mark_as_reserved(self, request, queryset):
#         queryset.update(status='reserved')
#         self.message_user(request, f'{queryset.count()} cargoes marked as reserved.')
#     mark_as_reserved.short_description = 'Mark as Reserved'
    
#     def mark_as_closed(self, request, queryset):
#         queryset.update(status='closed')
#         self.message_user(request, f'{queryset.count()} cargoes marked as closed.')
#     mark_as_closed.short_description = 'Mark as Closed'


# @admin.register(Transport)
# class TransportAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'title',
#         'carrier_info',
#         'location',
#         'available_from_date',
#         'transport_type',
#         'capacity_weight',
#         'price_info',
#         'status',
#         'views_count'
#     )
    
#     list_filter = (
#         'status',
#         'transport_type',
#         'available_from_date',
#         'created_at',
#         'has_gps',
#         'has_driver',
#     )
    
#     search_fields = (
#         'title',
#         'description',
#         'available_city_from',
#         'available_city_to',
#         'carrier__username',
#         'carrier__company_name',
#         'license_plate'
#     )
    
#     readonly_fields = (
#         'views_count', 
#         'contact_count', 
#         'created_at', 
#         'updated_at'
#     )
    
#     list_per_page = 25
#     date_hierarchy = 'created_at'
    
#     fieldsets = (
#         ('Basic Information', {
#             'fields': (
#                 'carrier',
#                 'title',
#                 'description',
#                 'status'
#             )
#         }),
#         ('Location & Availability', {
#             'fields': (
#                 'available_city_from',
#                 'available_city_to',
#                 'current_location',
#                 'available_from_date',
#                 'available_from_time',
#                 'available_to_date',
#                 'available_to_time',
#             )
#         }),
#         ('Vehicle Specifications', {
#             'fields': (
#                 'transport_type',
#                 'capacity_weight',
#                 'capacity_volume',
#                 'truck_model',
#                 'year',
#                 'license_plate',
#             )
#         }),
#         ('Pricing', {
#             'fields': (
#                 'price_per_km',
#                 'fixed_price',
#                 'price_negotiable',
#             )
#         }),
#         ('Features', {
#             'fields': (
#                 'has_gps',
#                 'has_driver',
#                 'has_temperature_control',
#                 'insurance_included',
#             ),
#             'classes': ('collapse',)
#         }),
#         ('Statistics', {
#             'fields': (
#                 'views_count',
#                 'contact_count',
#                 'created_at',
#                 'updated_at',
#                 'expires_at'
#             ),
#             'classes': ('collapse',)
#         }),
#     )
    
#     actions = ['mark_as_available', 'mark_as_booked', 'mark_as_unavailable']
    
#     def carrier_info(self, obj):
#         return format_html(
#             '{}<br><small>{}</small>',
#             obj.carrier.company_name or obj.carrier.username,
#             obj.carrier.email
#         )
#     carrier_info.short_description = 'Carrier'
#     carrier_info.admin_order_field = 'carrier__username'
    
#     def location(self, obj):
#         if obj.available_city_to:
#             return f"{obj.available_city_from} → {obj.available_city_to}"
#         return obj.available_city_from
#     location.short_description = 'Location'
    
#     def price_info(self, obj):
#         if obj.price_per_km:
#             price = f"${obj.price_per_km}/km"
#         elif obj.fixed_price:
#             price = f"${obj.fixed_price:,.2f}"
#         else:
#             price = 'Not specified'
        
#         if obj.price_negotiable and (obj.price_per_km or obj.fixed_price):
#             return f"{price} (negotiable)"
#         return price
#     price_info.short_description = 'Price'
    
#     def mark_as_available(self, request, queryset):
#         queryset.update(status='available')
#         self.message_user(request, f'{queryset.count()} transports marked as available.')
#     mark_as_available.short_description = 'Mark as Available'
    
#     def mark_as_booked(self, request, queryset):
#         queryset.update(status='booked')
#         self.message_user(request, f'{queryset.count()} transports marked as booked.')
#     mark_as_booked.short_description = 'Mark as Booked'
    
#     def mark_as_unavailable(self, request, queryset):
#         queryset.update(status='unavailable')
#         self.message_user(request, f'{queryset.count()} transports marked as unavailable.')
#     mark_as_unavailable.short_description = 'Mark as Unavailable'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'subject',
        'sender',
        'receiver',
        'related_listing',
        'is_read',
        'created_at'
    )
    
    list_filter = (
        'is_read',
        'created_at',
    )
    
    search_fields = (
        'subject',
        'content',
        'sender__username',
        'sender__email',
        'receiver__username',
        'receiver__email'
    )
    
    readonly_fields = ('created_at', 'read_at')
    list_per_page = 25
    
    fieldsets = (
        ('Message Details', {
            'fields': (
                'sender',
                'receiver',
                'subject',
                'content',
                'is_read',
                'read_at',
            )
        }),
        ('Related Listing', {
            'fields': (
                'cargo',
                'transport',
            ),
            'classes': ('collapse',)
        }),
        ('Thread', {
            'fields': (
                'parent_message',
                'is_deleted_by_sender',
                'is_deleted_by_receiver',
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def related_listing(self, obj):
        if obj.cargo:
            return f"📦 Cargo #{obj.cargo.id}"
        elif obj.transport:
            return f"🚛 Transport #{obj.transport.id}"
        return '-'
    related_listing.short_description = 'Related'
    
    def mark_as_read(self, request, queryset):
        for message in queryset:
            message.mark_as_read()
        self.message_user(request, f'{queryset.count()} messages marked as read.')
    mark_as_read.short_description = 'Mark as Read'
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False, read_at=None)
        self.message_user(request, f'{queryset.count()} messages marked as unread.')
    mark_as_unread.short_description = 'Mark as Unread'


@admin.register(ListingReport)
class ListingReportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'listing_info',
        'reported_by',
        'reason',
        'status',
        'created_at'
    )
    
    list_filter = (
        'reason',
        'status',
        'listing_type',
        'created_at'
    )
    
    search_fields = (
        'description',
        'reported_by__username',
        'reported_by__email'
    )
    
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Report Details', {
            'fields': (
                'listing_type',
                'listing_id',
                'reason',
                'description',
                'reported_by',
                'created_at',
            )
        }),
        ('Resolution', {
            'fields': (
                'status',
                'resolved_by',
                'resolved_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_reviewed', 'mark_as_resolved', 'mark_as_rejected']
    
    def listing_info(self, obj):
        if obj.listing_type == 'cargo':
            try:
                cargo = Cargo.objects.get(id=obj.listing_id)
                return f"📦 Cargo #{obj.listing_id}: {cargo.title[:30]}"
            except Cargo.DoesNotExist:
                return f"📦 Cargo #{obj.listing_id} (deleted)"
        else:
            try:
                transport = Transport.objects.get(id=obj.listing_id)
                return f"🚛 Transport #{obj.listing_id}: {transport.title[:30]}"
            except Transport.DoesNotExist:
                return f"🚛 Transport #{obj.listing_id} (deleted)"
    listing_info.short_description = 'Listing'
    
    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
        self.message_user(request, f'{queryset.count()} reports marked as reviewed.')
    mark_as_reviewed.short_description = 'Mark as Reviewed'
    
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved', resolved_by=request.user, resolved_at=timezone.now())
        self.message_user(request, f'{queryset.count()} reports marked as resolved.')
    mark_as_resolved.short_description = 'Mark as Resolved'
    
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected', resolved_by=request.user, resolved_at=timezone.now())
        self.message_user(request, f'{queryset.count()} reports rejected.')
    mark_as_rejected.short_description = 'Reject Reports'
    
    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.status in ['resolved', 'rejected']:
            if not obj.resolved_by:
                obj.resolved_by = request.user
            if not obj.resolved_at:
                obj.resolved_at = timezone.now()
        super().save_model(request, obj, form, change)