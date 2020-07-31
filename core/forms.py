from django import forms
from .models import UserPreferences,Preference


class UserPreferencesForm(forms.ModelForm):
    preferences = forms.ModelMultipleChoiceField(
        queryset=Preference.objects,
        widget=forms.CheckboxSelectMultiple,
        required=True, label="Choose your mailing list prefences :")

    class Meta:
        model = UserPreferences
        fields = ["preferences", ]
