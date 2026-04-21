from django import forms
from .models import (
    Cargo, CargoType, CargoStatus, 
    Transport, TransportType, TransportStatus,
    Message
)


class CargoForm(forms.ModelForm):
    """Form for creating and editing cargo listings"""
    
    class Meta:
        model = Cargo
        fields = [
            'title',
            'description',
            'pickup_city',
            'pickup_address',
            'delivery_city',
            'delivery_address',
            'pickup_date',
            'pickup_time',
            'delivery_date',
            'delivery_time',
            'weight',
            'volume',
            'cargo_type',
            'length',
            'width',
            'height',
            'price',
            'price_negotiable',
            'expires_at',
        ]
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'delivery_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'expires_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Electronics shipment from NY to LA'}),
            'pickup_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City name'}),
            'pickup_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street, building number'}),
            'delivery_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City name'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street, building number'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Weight in tons'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Volume in cubic meters'}),
            'length': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Length in meters'}),
            'width': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Width in meters'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Height in meters'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Offered price in USD'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make all required fields have proper styling
        for field_name, field in self.fields.items():
            if field_name not in ['price_negotiable']:
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'
        
        # Add checkbox class for boolean field
        self.fields['price_negotiable'].widget.attrs['class'] = 'form-check-input'
        
        # Make certain fields required explicitly
        required_fields = ['title', 'pickup_city', 'delivery_city', 'pickup_date', 'weight', 'cargo_type']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        pickup_date = cleaned_data.get('pickup_date')
        delivery_date = cleaned_data.get('delivery_date')
        
        if pickup_date and delivery_date and pickup_date > delivery_date:
            self.add_error('delivery_date', 'Delivery date cannot be earlier than pickup date')
        
        # Validate weight is positive
        weight = cleaned_data.get('weight')
        if weight and weight <= 0:
            self.add_error('weight', 'Weight must be greater than 0')
        
        return cleaned_data
    

class TransportForm(forms.ModelForm):
    """Form for creating and editing transport listings"""
    
    class Meta:
        model = Transport
        fields = [
            'title',
            'description',
            'available_city_from',
            'available_city_to',
            'current_location',
            'available_from_date',
            'available_from_time',
            'available_to_date',
            'available_to_time',
            'transport_type',
            'capacity_weight',
            'capacity_volume',
            'truck_model',
            'year',
            'license_plate',
            'price_per_km',
            'fixed_price',
            'price_negotiable',
            'has_gps',
            'has_driver',
            'has_temperature_control',
            'insurance_included',
            'expires_at',
        ]
        widgets = {
            'available_from_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'available_from_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'available_to_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'available_to_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'expires_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Volvo FH16 2023'}),
            'available_city_from': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City name'}),
            'available_city_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City name (optional)'}),
            'current_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current city'}),
            'truck_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Volvo FH16'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., ABC-123'}),
            'capacity_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Capacity in tons'}),
            'capacity_volume': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Volume in cubic meters'}),
            'price_per_km': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Price per kilometer in USD'}),
            'fixed_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Fixed price in USD'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2023'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Form-control class to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['price_negotiable', 'has_gps', 'has_driver', 'has_temperature_control', 'insurance_included']:
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'
        
        # Checkbox classes for boolean fields
        boolean_fields = ['price_negotiable', 'has_gps', 'has_driver', 'has_temperature_control', 'insurance_included']
        for field_name in boolean_fields:
            self.fields[field_name].widget.attrs['class'] = 'form-check-input'
        
        # Make certain fields required
        required_fields = ['title', 'available_city_from', 'available_from_date', 'transport_type', 'capacity_weight']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        available_from_date = cleaned_data.get('available_from_date')
        available_to_date = cleaned_data.get('available_to_date')
        
        if available_from_date and available_to_date and available_from_date > available_to_date:
            self.add_error('available_to_date', 'Available to date cannot be earlier than available from date')
        
        # Validate capacity weight is positive
        capacity_weight = cleaned_data.get('capacity_weight')
        if capacity_weight and capacity_weight <= 0:
            self.add_error('capacity_weight', 'Capacity must be greater than 0')
        
        # At least one price type should be provided
        price_per_km = cleaned_data.get('price_per_km')
        fixed_price = cleaned_data.get('fixed_price')
        
        if not price_per_km and not fixed_price:
            # Not an error, just optional
            pass
        
        return 
    

class MessageForm(forms.ModelForm):
    """Form for sending messages between users"""
    
    class Meta:
        model = Message
        fields = ['subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief subject of your message'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Type your message here...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].required = True
        self.fields['content'].required = True