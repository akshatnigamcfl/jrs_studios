from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    # path('home2', home2, name='home'),
    path('wedding', wedding, name='wedding'),
    path('cinematic', cinematic, name='cinematic'),
    path('pre-wedding', pre_wedding, name='pre-wedding'),
    path('pre-wedding/watch/<int:id>', pre_wedding_view, name='contact'),
    path('events', events, name='events'),
    path('reels', reels, name='reels'),
    path('team', team, name='team'),
    path('gallery', gallery, name='gallery'),
    path('booking', booking, name='booking'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('client-info/<int:client_id>/<str:client_token>', client_info, name='client_info'),
    path('client-info-confirm-booking/<int:client_id>/<str:client_token>', client_info_confirm_booking, name='client_info_confirm_booking'),
    path('scroller_test', scroller_test, name='scroller_test'),
    
    
]
