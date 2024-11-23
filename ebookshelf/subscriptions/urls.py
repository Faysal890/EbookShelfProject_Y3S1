from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('packages/', views.packages, name = 'packages'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]
