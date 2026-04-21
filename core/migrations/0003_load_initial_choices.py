# core/migrations/0002_load_initial_choices.py
from django.db import migrations

def create_initial_choices(apps, schema_editor):
    """
    Функция для заполнения начальными данными
    """
    # Получаем модели через apps.get_model (важно для миграций!)
    CargoStatus = apps.get_model('core', 'CargoStatus')
    CargoType = apps.get_model('core', 'CargoType')
    TransportStatus = apps.get_model('core', 'TransportStatus')
    TransportType = apps.get_model('core', 'TransportType')
    
    # Создаем статусы для грузов
    cargo_statuses = [
        {'name': 'Open', 'code': 'open', 'color': '#28a745', 'order': 1},
        {'name': 'Reserved', 'code': 'reserved', 'color': '#fd7e14', 'order': 2},
        {'name': 'In Transit', 'code': 'in_transit', 'color': '#007bff', 'order': 3},
        {'name': 'Delivered', 'code': 'delivered', 'color': '#6c757d', 'order': 4},
        {'name': 'Closed', 'code': 'closed', 'color': '#dc3545', 'order': 5},
        {'name': 'Cancelled', 'code': 'cancelled', 'color': '#8b0000', 'order': 6},
    ]
    
    for status_data in cargo_statuses:
        CargoStatus.objects.create(**status_data)
        print(f"Created cargo status: {status_data['name']}")
    
    # Создаем типы грузов
    cargo_types = [
        {'name': 'General Cargo', 'code': 'general', 'icon': '📦', 'order': 1},
        {'name': 'Pallets', 'code': 'pallet', 'icon': '📊', 'order': 2},
        {'name': 'Refrigerated', 'code': 'refrigerator', 'icon': '❄️', 'order': 3},
        {'name': 'Oversize', 'code': 'oversize', 'icon': '📏', 'order': 4},
        {'name': 'Hazardous', 'code': 'hazardous', 'icon': '⚠️', 'order': 5},
        {'name': 'Livestock', 'code': 'livestock', 'icon': '🐄', 'order': 6},
        {'name': 'Vehicles', 'code': 'vehicles', 'icon': '🚗', 'order': 7},
    ]
    
    for type_data in cargo_types:
        CargoType.objects.create(**type_data)
        print(f"Created cargo type: {type_data['name']}")
    
    # Создаем статусы для транспорта
    transport_statuses = [
        {'name': 'Available', 'code': 'available', 'color': '#28a745', 'order': 1},
        {'name': 'Booked', 'code': 'booked', 'color': '#fd7e14', 'order': 2},
        {'name': 'In Transit', 'code': 'in_transit', 'color': '#007bff', 'order': 3},
        {'name': 'Unavailable', 'code': 'unavailable', 'color': '#dc3545', 'order': 4},
    ]
    
    for status_data in transport_statuses:
        TransportStatus.objects.create(**status_data)
        print(f"Created transport status: {status_data['name']}")
    
    # Создаем типы транспорта
    transport_types = [
        {'name': 'Truck', 'code': 'truck', 'icon': '🚛', 'order': 1},
        {'name': 'Van', 'code': 'van', 'icon': '🚐', 'order': 2},
        {'name': 'Refrigerator Truck', 'code': 'refrigerator', 'icon': '❄️🚛', 'order': 3},
        {'name': 'Oversize Transport', 'code': 'oversize', 'icon': '📏🚛', 'order': 4},
        {'name': 'Trailer', 'code': 'trailer', 'icon': '🚛', 'order': 5},
        {'name': 'Container', 'code': 'container', 'icon': '📦', 'order': 6},
        {'name': 'Tanker', 'code': 'tanker', 'icon': '⛽', 'order': 7},
    ]
    
    for type_data in transport_types:
        TransportType.objects.create(**type_data)
        print(f"Created transport type: {type_data['name']}")

def remove_initial_choices(apps, schema_editor):
    """
    Функция для отката (удаления данных)
    """
    CargoStatus = apps.get_model('core', 'CargoStatus')
    CargoType = apps.get_model('core', 'CargoType')
    TransportStatus = apps.get_model('core', 'TransportStatus')
    TransportType = apps.get_model('core', 'TransportType')
    
    # Удаляем все данные
    CargoStatus.objects.all().delete()
    CargoType.objects.all().delete()
    TransportStatus.objects.all().delete()
    TransportType.objects.all().delete()
    
    print("All initial choices removed")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_cargostatus_cargotype_transportstatus_transporttype_and_more'),
    ]

    operations = [
        migrations.RunPython(create_initial_choices, remove_initial_choices),
    ]
