from django import forms
from .models import MembershipDetail, Donation,City
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_MODE_CHOICES = (
    ('O', 'One Time'),
    ('M', 'Monthly'),
)


class DonationForm(forms.ModelForm):
    payment_mode = forms.ChoiceField(
        choices=PAYMENT_MODE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Donation
        fields = ["payment_mode", "amount"]


class MembershipDetailForm(forms.ModelForm):

    first_name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'disabled': True}))
    last_name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'disabled': True}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'disabled': True}), required=False)
    city_name = forms.CharField(max_length=100, required=False,
                                label="If others,please specify:")
    # country = CountryField(blank_label='(Select country)').formfield(required=False,
                                                                    #  widget=CountrySelectWidget(attrs={'class': 'custom-select d-block w-100', 'id': 'shipping_country'}))

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
    # self.fields['city'].queryset = City.objects.none()
    # print('self.data =====================',self.data)

    # if 'country' in self.data:
    #     country_id = int(self.data.get('country'))
    #     cities = City.objects.filter(country__id=country_id).order_by('name')
    #     print
    #     self.fields['city'].queryset = City.objects.filter(country__id=country_id).order_by('name')


