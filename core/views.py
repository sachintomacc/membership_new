from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponse
from django.conf import settings
from .forms import UserPreferencesForm
import stripe
from .models import UserPreferences,Preference,UserProfile
from membership.models import MembershipDetail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


@login_required
def home(request):

    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.has_saved_preferences:
        response = redirect('dashboard')
    else:
        response = redirect('user_preferences')

    return response


@login_required
def dashboard(request):
    try:
        membership = MembershipDetail.objects.get(user=request.user)
        membership_type_name = membership.membership_type.type_name
    except:
        membership_type_name = None
    context = {'membership_type_name':membership_type_name}
    return render(request, 'dashboard.html',context)


@login_required
def user_preferences(request):
    form = UserPreferencesForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user  = request.user
        instance.save()
        form.save_m2m()
        messages.success(request,'Your preferences has been saved !')
        return redirect('thankyou')

    context = {'form': form, 'username':request.user.username}
    return render(request, 'user_preferences.html', context)


def thankyou(request):
    return render(request, 'thankyou.html')
