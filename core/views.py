from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import (
    Cargo, CargoType, CargoStatus,
    Transport, TransportType, TransportStatus,
    Message
)
from accounts.models import User
from .forms import CargoForm, TransportForm, MessageForm
from django.utils import timezone


def home(request):
    """
    Home page
    """
    return render(request, 'base/home.html')


def how_it_works(request):
    """
    Static page explaining how the platform works
    """
    return render(request, 'core/how_it_works.html', {
        'title': 'How It Works'
    })


def contact(request):
    """
    Static page with contact information
    """
    return render(request, 'core/contact.html', {
        'title': 'Contact Us'
    })


#################################
# Load (Cargo) Views for Shipper
#################################

@login_required
def post_load(request):
    """
    View for shippers to post new cargo listings
    """
    # Check if user is shipper
    if request.user.role != 'shipper':
        messages.error(request, 'Only shippers can post cargo listings.')
        return redirect('home')
    
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            cargo = form.save(commit=False)
            cargo.shipper = request.user
            # Set initial status
            try:
                open_status = CargoStatus.objects.get(code='open')
                cargo.status = open_status
            except CargoStatus.DoesNotExist:
                messages.error(request, 'System error: Cargo status not found. Please contact administrator.')
                return redirect('home')
            
            cargo.save()
            messages.success(request, 'Your load has been posted successfully!')
            return redirect('my_loads')
        else:
            # Print form errors to console for debugging
            print("Form errors:", form.errors)
            # Add error message for user
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CargoForm()
    
    return render(request, 'core/post_load.html', {
        'form': form, 
        'title': 'Post New Load'
    })


@login_required
def my_loads(request):
    """
    View for shippers to view and manage their cargo listings
    """
    if request.user.role != 'shipper':
        messages.error(request, 'Only shippers can view their loads.')
        return redirect('home')
    
    cargoes = Cargo.objects.filter(shipper=request.user).select_related('cargo_type', 'status')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        cargoes = cargoes.filter(status__code=status_filter)
    
    paginator = Paginator(cargoes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/my_loads.html', {
        'page_obj': page_obj,
        'cargoes': page_obj.object_list,
        'title': 'My Loads'
    })


@login_required
def edit_load(request, pk):
    """
    View for shippers to edit their cargo listings
    """
    cargo = get_object_or_404(Cargo, pk=pk, shipper=request.user)
    
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your load has been updated successfully!')
            return redirect('my_loads')
    else:
        form = CargoForm(instance=cargo)
    
    return render(request, 'core/post_load.html', {
        'form': form, 
        'title': 'Edit Load',
        'cargo': cargo
    })


@login_required
def delete_load(request, pk):
    """
    View for shippers to delete their cargo listings
    """
    cargo = get_object_or_404(Cargo, pk=pk, shipper=request.user)
    
    if request.method == 'POST':
        cargo.delete()
        messages.success(request, 'Your load has been deleted successfully!')
        return redirect('my_loads')
    
    return render(request, 'core/confirm_delete.html', {
        'object': cargo,
        'title': 'Delete Load',
        'type': 'load'
    })


def browse_loads(request):
    """
    Public view for carriers to browse available cargo listings
    """
    # Get all active cargoes (open status and not expired)
    cargoes = Cargo.objects.filter(status__code='open').select_related('shipper', 'cargo_type', 'status')
    
    # Filter by pickup city
    pickup_city = request.GET.get('pickup_city')
    if pickup_city:
        cargoes = cargoes.filter(pickup_city__icontains=pickup_city)
    
    # Filter by delivery city
    delivery_city = request.GET.get('delivery_city')
    if delivery_city:
        cargoes = cargoes.filter(delivery_city__icontains=delivery_city)
    
    # Filter by cargo type
    cargo_type = request.GET.get('cargo_type')
    if cargo_type:
        cargoes = cargoes.filter(cargo_type__code=cargo_type)
    
    # Filter by min/max weight
    min_weight = request.GET.get('min_weight')
    if min_weight:
        cargoes = cargoes.filter(weight__gte=min_weight)
    
    max_weight = request.GET.get('max_weight')
    if max_weight:
        cargoes = cargoes.filter(weight__lte=max_weight)
    
    # Order by creation date (newest first)
    cargoes = cargoes.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(cargoes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all cargo types for filter dropdown
    cargo_types = CargoType.objects.filter(is_active=True)
    
    return render(request, 'core/browse_loads.html', {
        'page_obj': page_obj,
        'cargoes': page_obj.object_list,
        'cargo_types': cargo_types,
        'title': 'Browse Loads'
    })


def load_detail(request, pk):
    """
    Public view for viewing detailed cargo information
    """
    cargo = get_object_or_404(Cargo, pk=pk)
    
    # Increment view count
    cargo.views_count += 1
    cargo.save(update_fields=['views_count'])
    
    return render(request, 'core/load_detail.html', {
        'cargo': cargo,
        'title': cargo.title
    })

#################################
# Transport Views for Carrier
#################################

@login_required
def post_truck(request):
    """
    View for carriers to post new transport listings
    """
    # Check if user is carrier
    if request.user.role != 'carrier':
        messages.error(request, 'Only carriers can post transport listings.')
        return redirect('home')
    
    if request.method == 'POST':
        form = TransportForm(request.POST)
        if form.is_valid():
            transport = form.save(commit=False)
            transport.carrier = request.user
            # Set initial status
            try:
                available_status = TransportStatus.objects.get(code='available')
                transport.status = available_status
            except TransportStatus.DoesNotExist:
                messages.error(request, 'System error: Transport status not found. Please contact administrator.')
                return redirect('home')
            
            transport.save()
            messages.success(request, 'Your transport listing has been posted successfully!')
            return redirect('my_trucks')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TransportForm()
    
    return render(request, 'core/post_truck.html', {
        'form': form, 
        'title': 'Post Available Truck'
    })


@login_required
def my_trucks(request):
    """
    View for carriers to view and manage their transport listings
    """
    if request.user.role != 'carrier':
        messages.error(request, 'Only carriers can view their trucks.')
        return redirect('home')
    
    transports = Transport.objects.filter(carrier=request.user).select_related('transport_type', 'status')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        transports = transports.filter(status__code=status_filter)
    
    paginator = Paginator(transports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/my_trucks.html', {
        'page_obj': page_obj,
        'transports': page_obj.object_list,
        'title': 'My Trucks'
    })


@login_required
def edit_truck(request, pk):
    """
    View for carriers to edit their transport listings
    """
    transport = get_object_or_404(Transport, pk=pk, carrier=request.user)
    
    if request.method == 'POST':
        form = TransportForm(request.POST, instance=transport)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your transport listing has been updated successfully!')
            return redirect('my_trucks')
    else:
        form = TransportForm(instance=transport)
    
    return render(request, 'core/post_truck.html', {
        'form': form, 
        'title': 'Edit Truck',
        'transport': transport
    })


@login_required
def delete_truck(request, pk):
    """
    View for carriers to delete their transport listings
    """
    transport = get_object_or_404(Transport, pk=pk, carrier=request.user)
    
    if request.method == 'POST':
        transport.delete()
        messages.success(request, 'Your transport listing has been deleted successfully!')
        return redirect('my_trucks')
    
    return render(request, 'core/confirm_delete.html', {
        'object': transport,
        'title': 'Delete Truck',
        'type': 'truck'
    })


def browse_trucks(request):
    """
    Public view for shippers to browse available transport listings
    """
    # Get all available transports
    transports = Transport.objects.filter(status__code='available').select_related('carrier', 'transport_type', 'status')
    
    # Filter by city
    city_from = request.GET.get('city_from')
    if city_from:
        transports = transports.filter(available_city_from__icontains=city_from)
    
    # Filter by transport type
    transport_type = request.GET.get('transport_type')
    if transport_type:
        transports = transports.filter(transport_type__code=transport_type)
    
    # Filter by min/max capacity
    min_capacity = request.GET.get('min_capacity')
    if min_capacity:
        transports = transports.filter(capacity_weight__gte=min_capacity)
    
    max_capacity = request.GET.get('max_capacity')
    if max_capacity:
        transports = transports.filter(capacity_weight__lte=max_capacity)
    
    # Filter by features
    has_gps = request.GET.get('has_gps')
    if has_gps == 'on':
        transports = transports.filter(has_gps=True)
    
    has_temperature = request.GET.get('has_temperature')
    if has_temperature == 'on':
        transports = transports.filter(has_temperature_control=True)
    
    # Order by creation date (newest first)
    transports = transports.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(transports, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all transport types for filter dropdown
    transport_types = TransportType.objects.filter(is_active=True)
    
    return render(request, 'core/browse_trucks.html', {
        'page_obj': page_obj,
        'transports': page_obj.object_list,
        'transport_types': transport_types,
        'title': 'Browse Transport'
    })


def truck_detail(request, pk):
    """
    Public view for viewing detailed transport information
    """
    transport = get_object_or_404(Transport, pk=pk)
    
    # Increment view count
    transport.views_count += 1
    transport.save(update_fields=['views_count'])
    
    return render(request, 'core/truck_detail.html', {
        'transport': transport,
        'title': transport.title
    })


@login_required
def send_message(request, listing_type, listing_id):
    """
    Send a message about a specific listing (cargo or transport)
    """
    # Get the listing and determine receiver
    if listing_type == 'cargo':
        listing = get_object_or_404(Cargo, pk=listing_id)
        receiver = listing.shipper
        listing_obj = listing
        redirect_url = 'load_detail'  # Используем имя URL
    elif listing_type == 'transport':
        listing = get_object_or_404(Transport, pk=listing_id)
        receiver = listing.carrier
        listing_obj = listing
        redirect_url = 'truck_detail'  # Используем имя URL
    else:
        messages.error(request, 'Invalid listing type.')
        return redirect('home')
    
    # Can't send message to yourself
    if request.user == receiver:
        messages.warning(request, 'You cannot send a message to yourself.')
        return redirect(redirect_url, pk=listing_id)  # Исправлено
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            
            # Link to the listing
            if listing_type == 'cargo':
                message.cargo = listing_obj
            else:
                message.transport = listing_obj
            
            # Auto-generate subject if empty
            if not message.subject:
                message.subject = f"Inquiry about {listing_obj.title}"
            
            message.save()
            messages.success(request, f'Your message has been sent to {receiver.get_full_name() or receiver.username}!')
            
            # Redirect back to the listing detail - исправлено
            return redirect(redirect_url, pk=listing_id)
    else:
        # Pre-fill the subject
        initial_subject = f"Inquiry about {listing_obj.title}"
        form = MessageForm(initial={'subject': initial_subject})
    
    context = {
        'form': form,
        'listing': listing_obj,
        'listing_type': listing_type,
        'receiver': receiver,
        'title': f'Send Message about {listing_obj.title}'
    }
    return render(request, 'core/send_message.html', context)


@login_required
def message_inbox(request):
    """
    View all received messages
    """
    # Get messages where user is receiver and not deleted
    received_messages = Message.objects.filter(
        receiver=request.user,
        is_deleted_by_receiver=False
    ).select_related('sender', 'cargo', 'transport')
    
    # Get messages where user is sender (for sent folder)
    sent_messages = Message.objects.filter(
        sender=request.user,
        is_deleted_by_sender=False
    ).select_related('receiver', 'cargo', 'transport')
    
    # Get unread count
    unread_count = received_messages.filter(is_read=False).count()
    
    # Pagination for received messages
    paginator = Paginator(received_messages, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/message_inbox.html', {
        'page_obj': page_obj,
        'messages': page_obj.object_list,
        'sent_messages': sent_messages[:10],  # Last 10 sent messages
        'unread_count': unread_count,
        'title': 'Messages'
    })


@login_required
def message_detail(request, pk):
    """
    View a single message and mark it as read
    """
    message = get_object_or_404(Message, pk=pk)
    
    # Check if user is sender or receiver
    if request.user not in [message.sender, message.receiver]:
        messages.error(request, 'You do not have permission to view this message.')
        return redirect('message_inbox')
    
    # Mark as read if user is receiver
    if request.user == message.receiver and not message.is_read:
        message.mark_as_read()
    
    # Handle reply
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.receiver = message.sender if request.user == message.receiver else message.receiver
            reply.parent_message = message
            # Auto-generate subject with Re:
            reply.subject = f"Re: {message.subject}"
            
            # Copy listing references
            reply.cargo = message.cargo
            reply.transport = message.transport
            
            reply.save()
            messages.success(request, 'Your reply has been sent successfully!')
            # Redirect to inbox instead of back to the same message
            return redirect('message_inbox')
        else:
            # Print errors to console for debugging
            print("Form errors:", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill subject for reply
        initial_subject = f"Re: {message.subject}"
        form = MessageForm(initial={'subject': initial_subject})
    
    return render(request, 'core/message_detail.html', {
        'message': message,
        'form': form,
        'title': 'Message Details'
    })


@login_required
def delete_message(request, pk):
    """
    Soft delete a message (mark as deleted for user)
    """
    message = get_object_or_404(Message, pk=pk)
    
    if request.user == message.sender:
        message.is_deleted_by_sender = True
        message.save()
        messages.success(request, 'Message deleted.')
    elif request.user == message.receiver:
        message.is_deleted_by_receiver = True
        message.save()
        messages.success(request, 'Message deleted.')
    else:
        messages.error(request, 'You do not have permission to delete this message.')
    
    return redirect('message_inbox')


@login_required
def mark_as_read(request, pk):
    """
    Mark a single message as read
    """
    message = get_object_or_404(Message, pk=pk, receiver=request.user)
    message.mark_as_read()
    messages.success(request, 'Message marked as read.')
    return redirect('message_detail', pk=message.pk)


def browse_listings(request):
    """
    Unified page to browse all active listings (cargo and transport)
    """
    # Get all active cargoes (open status)
    cargoes = Cargo.objects.filter(
        status__code='open'
    ).select_related('shipper', 'cargo_type', 'status')[:20]  # Limit to 20 for demo
    
    # Get all available transports
    transports = Transport.objects.filter(
        status__code='available'
    ).select_related('carrier', 'transport_type', 'status')[:20]  # Limit to 20 for demo
    
    # Combine into a single list with type indicator
    all_listings = []
    
    for cargo in cargoes:
        all_listings.append({
            'id': cargo.id,
            'type': 'cargo',
            'type_icon': 'bi bi-box-seam',
            'type_name': 'Load',
            'title': cargo.title,
            'description': cargo.description[:150],
            'location_from': cargo.pickup_city,
            'location_to': cargo.delivery_city,
            'date': cargo.pickup_date,
            'company': cargo.shipper.company_name or cargo.shipper.username,
            'price': cargo.price,
            'weight': cargo.weight,
            'status': cargo.status.name,
            'views': cargo.views_count,
            'detail_url': f'/loads/{cargo.id}/'
        })
    
    for transport in transports:
        all_listings.append({
            'id': transport.id,
            'type': 'transport',
            'type_icon': 'bi bi-truck',
            'type_name': 'Transport',
            'title': transport.title,
            'description': transport.description[:150],
            'location_from': transport.available_city_from,
            'location_to': transport.available_city_to or 'Any',
            'date': transport.available_from_date,
            'company': transport.carrier.company_name or transport.carrier.username,
            'price': transport.price_per_km or transport.fixed_price,
            'weight': transport.capacity_weight,
            'status': transport.status.name,
            'views': transport.views_count,
            'detail_url': f'/trucks/{transport.id}/'
        })
    
    # Sort by date (newest first)
    all_listings.sort(key=lambda x: x['date'], reverse=True)
    
    # Pagination
    paginator = Paginator(all_listings, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get statistics for the page
    stats = {
        'total_loads': Cargo.objects.filter(status__code='open').count(),
        'total_trucks': Transport.objects.filter(status__code='available').count(),
        'total_companies': User.objects.filter(is_approved=True).exclude(role='admin').count(),
    }
    
    return render(request, 'core/browse_listings.html', {
        'page_obj': page_obj,
        'listings': page_obj.object_list,
        'stats': stats,
        'title': 'Browse All Listings'
    })