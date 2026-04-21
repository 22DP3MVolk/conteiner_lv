from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [

    path('', views.home, name='home'),

    # Static Pages
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('contact/', views.contact, name='contact'),

    # Cargo (Load) URLs
    path('loads/post/', views.post_load, name='post_load'),
    path('loads/my/', views.my_loads, name='my_loads'),
    path('loads/edit/<int:pk>/', views.edit_load, name='edit_load'),
    path('loads/delete/<int:pk>/', views.delete_load, name='delete_load'),
    path('loads/browse/', views.browse_loads, name='browse_loads'),
    path('loads/<int:pk>/', views.load_detail, name='load_detail'),

    # Transport (Truck) URLs
    path('trucks/post/', views.post_truck, name='post_truck'),
    path('trucks/my/', views.my_trucks, name='my_trucks'),
    path('trucks/edit/<int:pk>/', views.edit_truck, name='edit_truck'),
    path('trucks/delete/<int:pk>/', views.delete_truck, name='delete_truck'),
    path('trucks/browse/', views.browse_trucks, name='browse_trucks'),
    path('trucks/<int:pk>/', views.truck_detail, name='truck_detail'),

    # Message URLs
    path('messages/send/<str:listing_type>/<int:listing_id>/', views.send_message, name='send_message'),
    path('messages/inbox/', views.message_inbox, name='message_inbox'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/delete/<int:pk>/', views.delete_message, name='delete_message'),
    path('messages/read/<int:pk>/', views.mark_as_read, name='mark_as_read'),

    # Browse all listings (unified page)
    path('browse/', views.browse_listings, name='browse_listings'),

]