from django.contrib import admin
from django.urls import path, include
from core.views import *#home,  thankyou, dashboard, user_preferences
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('user_preferences/', user_preferences, name='user_preferences'),
    path('thankyou/', thankyou, name='thankyou'),
    path('page_not_found/', page_not_found, name='page_not_found'),
    path('error/', error, name='error'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),



]
