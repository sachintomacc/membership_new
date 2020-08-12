from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(MembershipDetail)
admin.site.register(MembershipType)
admin.site.register(MemberPaymentHistory)
admin.site.register(City)
admin.site.register(Title)
admin.site.register(Country)
admin.site.register(Donation)