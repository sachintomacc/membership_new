from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_profile')
    is_member = models.BooleanField(default=False)
    has_saved_preferences = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=20, null=True, blank=True)
    stripe_membership_subscription_id = models.CharField(
        max_length=20, null=True, blank=True)
    stripe_donation_subscription_id = models.CharField(
        max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)


class Preference(models.Model):
    option = models.CharField(max_length=50)

    def __str__(self):
        return self.option


class UserPreferences(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_preferences')
    preferences = models.ManyToManyField(Preference)

    def __str__(self):
        return self.user.username


class Setting(models.Model):
    name = models.CharField(max_length=50)
    value = models.TextField()


def __str__(self):
    return self.name
