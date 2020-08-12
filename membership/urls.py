from django.contrib import admin
from django.urls import path, include
from .views import (create_membership, membership, stripe_payment, cancel_subscription,
                    create_donation, donation, payment_history, subscriptions, gold_page,load_cities,
                    silver_page,
                    bronze_page)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('stripe_payment/', stripe_payment, name='stripe_payment'),
    path('membership/', membership, name='membership'),
    path('create_membership/', create_membership, name='create_membership'),
    path('donation/', donation, name='donation'),
    path('create_donation/', create_donation, name='create_donation'),
    path('payment_history/', payment_history, name='payment_history'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('cancel_subscription/<str:subscription_type>/',
         cancel_subscription, name='cancel_subscription'),
    path('gold_page/', gold_page, name='gold_page'),
    path('silver_page/', silver_page, name='silver_page'),
    path('bronze_page/', bronze_page, name='bronze_page'),
    path('stripe/',include('djstripe.urls')),
    path('ajax_load_cities/' , load_cities , name='ajax_load_cities'),
]
