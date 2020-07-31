from django.contrib import admin
from django.urls import path, include
from .views import membership,  stripee_create_membership, stripee_create_donation,stripee_two, chargeCustomer, create_donation, donation,payment_history
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('membership/', membership, name='membership'),
    path('membership-payment/', stripee_create_membership, name='stripee_create_membership'),
    path('donation-payment/', stripee_create_donation, name='stripee_create_donation'),
    # path('stripee/<payment_type>', StripeView.as_view(), name='stripee'),
    path('stripee_two/', stripee_two, name='stripee_two'),
    path('charge/', chargeCustomer, name='create_membership'),
    path('donate/', create_donation, name='create_donation'),
    path('donation/', donation, name='donation'),
    path('payment_history/', payment_history, name='payment_history'),
]
