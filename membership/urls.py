from django.contrib import admin
from django.urls import path, include
from .views import (create_membership, membership, stripe_payment,
                    create_donation, donation, payment_history,subscriptions)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('stripe_payment/', stripe_payment, name='stripe_payment'),
    path('membership/', membership, name='membership'),
    path('create_membership/', create_membership, name='create_membership'),
    path('donation/', donation, name='donation'),
    path('create_donation/', create_donation, name='create_donation'),
    path('payment_history/', payment_history, name='payment_history'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]
