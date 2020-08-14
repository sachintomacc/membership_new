from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField

User = get_user_model()
TERM_CHOICES = (
    ('M', 'Monthly'),
    ('Y', 'Yearly'),
)

DONATION_CHOICES = (
    ('M', 'Monthly'),
    ('O', 'One Time'),
)


class MembershipDetail(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='member', null=True, blank=True)
    membership_type = models.ForeignKey(
        'MembershipType', on_delete=models.CASCADE)
    membership_term = models.CharField(max_length=50, choices=TERM_CHOICES)
    title = models.ForeignKey(
        'Title', on_delete=models.SET_NULL, null=True, default=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.ForeignKey(
        'City', on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(
        'Country', on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(max_length=254)
    telephone = models.IntegerField()
    date_joined = models.DateField()
    date_terminated = models.DateField(null=True, blank=True)
    is_paid_up = models.BooleanField()
    notes = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'MembershipDetail'
        verbose_name_plural = 'MembershipDetails'

    def __str__(self):
        return self.user.username


class MembershipType(models.Model):
    name = models.CharField(max_length=50)
    stripe_monthly_price_id = models.CharField(
        max_length=50, null=True, blank=True)
    stripe_yearly_price_id = models.CharField(
        max_length=50, null=True, blank=True)

    class Meta:

        verbose_name = 'MembershipType'
        verbose_name_plural = 'MembershipTypes'

    def __str__(self):
        return self.name


class MemberPaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=25)
    amount = models.FloatField()
    description = models.CharField(max_length=50, null=True, blank=True)
    payment_date = models.DateField(auto_now_add=True)

    class Meta:

        verbose_name = 'MemberPaymentHistory'
        verbose_name_plural = 'MemberPaymentHistories'

    def __str__(self):
        return self.user.username


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.name


class Donation(models.Model):
    payment_mode = models.CharField(max_length=50)
    amount = models.FloatField()
    email = models.EmailField(max_length=254)
    stripe_donation_subscription_id = models.CharField(
        max_length=20, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='donated_user', null=True, blank=True)
