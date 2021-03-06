from django import forms
from .models import MembershipDetail, Donation, City
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_MODE_CHOICES = (
    ('O', 'One Time'),
    ('M', 'Monthly'),
)


class DonationForm(forms.ModelForm):
    payment_mode = forms.ChoiceField(
        choices=PAYMENT_MODE_CHOICES, widget=forms.RadioSelect())
    is_anonymous = forms.BooleanField(
        label="Donate anonymously", required=False)

    class Meta:
        model = Donation
        fields = ["is_anonymous", "payment_mode", "amount"]

def __init__(self, *args, **kwargs):
	super().__init__(*args, **kwargs)
	self.fields['payment_mode'].required = True

	



class MembershipDetailForm(forms.ModelForm):

    first_name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'disabled': True}))
    last_name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'disabled': True}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'disabled': True}), required=False)
    city_name = forms.CharField(max_length=100, required=False,
                                label="If others,please specify:")

    class Meta:
        model = MembershipDetail
        # fields = "__all__"
        fields = ["membership_type", "membership_term", "title", "country",
                  "first_name", "last_name", "email", "address", "city", "city_name", "telephone"]


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['title'].required = True
    self.fields['country'].required = True
    self.fields['city_name'].required = False
