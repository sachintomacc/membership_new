from django.contrib import admin
from .models import *



admin.site.register(UserProfile)
admin.site.register(UserPreferences)
admin.site.register(Preference)