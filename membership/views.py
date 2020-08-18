from membership.templatetags.define_action import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from stripe.api_resources import subscription
from stripe.api_resources.billing_portal import session
from stripe.api_resources.exchange_rate import ExchangeRate
from .forms import MembershipDetailForm, DonationForm
from django.conf import settings
from .models import *
from django.contrib import messages
from django.contrib.auth.models import Group
from django.views.generic import View
from django.contrib.auth.decorators import login_required
import stripe
import datetime
import random
import string
from django.core.exceptions import ObjectDoesNotExist
from core.models import UserProfile, Setting
from django.db.models import Sum
from membership.decorators import allowed_users
from django.dispatch import receiver
from djstripe.signals import WEBHOOK_SIGNALS
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import JsonResponse
stripe.api_key = settings.STRIPE_KEY


def get_setting(name, default_value):
    try:
        return Setting.objects.get(name=name).value
    except:
        return default_value


def donation(request):
    if request.method == 'POST':
        print('POST = ', request.POST)
        form = DonationForm(request.POST)
        if form.is_valid():
            request.session['DonationDetails'] = request.POST
            request.session['payment_type'] = 'donation'
            return redirect('stripe_payment')

    form = DonationForm()
    donations = Donation.objects.all().count()
    total_raised = int(Donation.objects.aggregate(
        Sum('amount')).get('amount__sum'))
    print('total_raised = ', total_raised)

    context = {'form': form, 'donations': donations,
               'total_raised': total_raised}

    return render(request, 'donation.html', context)


@login_required
def membership(request):

    if request.method == 'POST':
        form = MembershipDetailForm(request.POST)
        if form.is_valid():
            request.session['MembershipDetails'] = request.POST
            request.session['payment_type'] = 'membership'
            return redirect('stripe_payment')
        else:
            print('invalid')
            context = {'form': form}
            return render(request, 'membership.html', context)

    form_intial_values = {
        'first_name': request.user.first_name, 'last_name': request.user.last_name, 'email': request.user.email}
    form = MembershipDetailForm(initial=form_intial_values)
    context = {'form': form}
    return render(request, 'membership.html', context)


def create_donation(request):
    print('POST==', request.POST)
    amount = int(request.session['DonationDetails'].get('amount'))

    try:
        if 'is_anonymous'  in request.session['DonationDetails']:
            user = None
            email = ''
            donor_name = None
            is_anonymous = True
            is_member = False
            customer = stripe.Customer.create(source=request.POST['stripeToken'])
            stripe_customer_id = customer.id

        else:
            email=request.POST['email']
            donor_name = request.POST['name']
            is_anonymous = False
            try:
            # if yes,get stripe customer id
                user_profile = UserProfile.objects.exclude(stripe_customer_id__isnull=True).exclude(
                    stripe_customer_id__exact='').get(user__email=request.POST.get('email'))
                stripe_customer_id = user_profile.stripe_customer_id
                user = request.user
                is_member = True
            except ObjectDoesNotExist as e :
                # else,create a new stripe customer and store the stripe customer id
                customer = stripe.Customer.create(
                    email=request.POST['email'], name=request.POST['name'], source=request.POST['stripeToken'])
                stripe_customer_id = customer.id
                user = None
                is_member = False
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',str(e))

        if request.session['DonationDetails'].get('payment_mode') == 'O':
            description = 'One time donation',
            stripe.Charge.create(
                amount=amount*100,
                currency="inr",
                customer=stripe_customer_id
            )
            stripe_donation_subscription_id =None
        else:
            description = 'Monthly donation',
            stripe_donation_product_id = get_setting('STRIPE_DONATION_PRODUCT_ID', '')
            customer = stripe.Customer.create(source=request.POST['stripeToken'])
            subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{
                'price_data': {
                    'unit_amount': amount*100,
                    'currency': 'inr',
                    'product': stripe_donation_product_id,
                    'recurring': {
                        'interval': 'month',
                    },
                },
            }],
            )
            stripe_donation_subscription_id = subscription.id
        

        log_donations(user, amount, description, str(request.session['DonationDetails'].get('payment_mode')), email, stripe_donation_subscription_id,donor_name,is_anonymous)

        if is_member:
            log_to_member_payment_history(user, amount, description)
            user_profile.stripe_donation_subscription_id = stripe_donation_subscription_id
            user_profile.save()
        
        messages.success(request,'Your donation has been received !')
        return redirect('thankyou')
    except Exception as e:
        messages.warning(request,str(e))
        return redirect('error')


def create_membership(request):

    print('POST = ', request.POST)
    amount = int(request.session['DonationDetails'].get('amount'))*100

    try:
        # fetching the memebership type
        membership_type = MembershipType.objects.get(
            id=int(request.session['MembershipDetails'].get('membership_type')))

        # fetching memebership term and corresponding details
        if request.session['MembershipDetails'].get('membership_term') == 'M':
            price_id = membership_type.stripe_monthly_price_id
            amount = get_stripe_price_details(price_id)
            description = membership_type.name + ' Monthly Plan Payment'

        elif request.session['MembershipDetails'].get('membership_term') == 'Y':
            price_id = membership_type.stripe_yearly_price_id
            amount = get_stripe_price_details(price_id)
            description = membership_type.name + ' Yearly Plan Payment'

        country = Country.objects.get(
            id=int(request.session['MembershipDetails'].get('country')))

        # creating a new city and adding it to MembershipDetail if user enters a custom city name
        if request.session['MembershipDetails'].get('city_name') != '':
            new_city = City.objects.create(
                name=request.session['MembershipDetails'].get('city_name'), country=country)
            user_city = new_city

        else:
            user_city = City.objects.get(
                id=int(request.session['MembershipDetails'].get('city')))
    except Exception as e:
        print(e)
        messages.error(request, str(e))
        return redirect('error')

    try:
        # creating a stripe customer
        customer = stripe.Customer.create(
            email=request.session['MembershipDetails'].get('email'), name=f'{request.user.first_name} {request.user.last_name}', source=request.POST['stripeToken'])

        # creating a stripe subscription
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {"price": price_id},
            ],
        )

        # creating membership detail record
        user_membership_detail = MembershipDetail.objects.create(user=request.user, membership_type=membership_type, membership_term=request.session['MembershipDetails'].get('membership_term'),
                                                                 title=Title.objects.get(
            id=int(request.session['MembershipDetails'].get('title'))),
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            city=user_city,
            address=request.session['MembershipDetails'].get(
            'address'),
            country=country,
            email=request.user.email,
            telephone=request.session['MembershipDetails'].get(
            'telephone'),
            date_joined=datetime.date.today(),
            is_paid_up=True
        )

        # fetching the group to enable Restricted View Feature
        membership_group = Group.objects.get(name=membership_type.name)
        # adding the group to the user
        request.user.groups.add(membership_group)

        # updaing membership related attributes is user profile
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.stripe_customer_id = customer.id
        user_profile.stripe_membership_subscription_id = subscription.id
        user_profile.is_member = True
        user_profile.save()

        # logging the above payment to membership payment table
        log_to_member_payment_history(request.user, amount, description)

        # clearing the session values
        del request.session['MembershipDetails']
        del request.session['payment_type']
        request.session.modified = True

        messages.success(request, 'Your membership has been activated !')
        return redirect(reverse('thankyou'))

    # stripe payment exceptions
    except stripe.error.CardError as e:
        messages.error(request, 'CardError')
        return redirect('error')
    except stripe.error.RateLimitError as e:
        messages.error(request, 'RateLimitError')
        return redirect('error')
    except stripe.error.InvalidRequestError as e:
        messages.error(request, 'InvalidRequestError')
        return redirect('error')
    except stripe.error.AuthenticationError as e:
        messages.error(request, 'AuthenticationError')
        return redirect('error')
    except stripe.error.APIConnectionError as e:
        messages.error(request, 'APIConnectionError')
        return redirect('error')
    except stripe.error.StripeError as e:
        messages.error(request, 'StripeError')
        return redirect('error')
    except Exception as e:
        messages.error(request, e)
        return redirect('error')


# function to create records in Member Payment History table
def log_to_member_payment_history(user, amount, description):
    MemberPaymentHistory.objects.create(
        user=user, ref_code=create_ref_code(), amount=amount, description=description)
    return

# function to create records in Donation table


def log_donations(user, amount, description, payment_mode, email, stripe_donation_subscription_id,donor_name,is_anonymous):
    print('description=', description, 'mode=', payment_mode,)
    Donation.objects.create(
        payment_mode=payment_mode, amount=amount, donor_name=donor_name, donor_email=email, stripe_donation_subscription_id=stripe_donation_subscription_id, user=user)
    return

# function to create a unique ref code for each trransaction


def create_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))


# view to display payment history of member
@login_required
def payment_history(request):
    payments = MemberPaymentHistory.objects.filter(user=request.user)
    context = {'payments': payments}

    return render(request, 'payment_history.html', context)


# view to display active subscriptions
@login_required
def subscriptions(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}

    return render(request, 'subscriptions.html', context)

# view for stripe payment to enter Card details


def stripe_payment(request):
    return render(request, 'stripe_payment.html')


# method to cancel membership/donation subscription
def cancel_subscription(request, subscription_type):
    user_profile = UserProfile.objects.get(user=request.user)

    if subscription_type == 'membership':
        subscription_id = user_profile.stripe_membership_subscription_id
        user_profile.stripe_membership_subscription_id = ''
    else:
        subscription_id = user_profile.stripe_donation_subscription_id
        user_profile.stripe_membership_subscription_id = ''

    stripe.Subscription.delete(subscription_id)
    user_profile.save()

    messages.info(request, 'Your subscription has been cancelled')
    return redirect('thankyou')


# the view which is accessible only for Gold members
@login_required
@allowed_users(allowed_roles=['Gold'])
def gold_page(request):
    return render(request, 'gold_page.html')


# the view which is accessible only for Silver members
@login_required
@allowed_users(allowed_roles=['Silver'])
def silver_page(request):
    return render(request, 'silver_page.html')


# the view which is accessible only for Bronze members
@login_required
@allowed_users(allowed_roles=['Bronze'])
def bronze_page(request):
    return render(request, 'bronze_page.html')

# funtion tied to the webhook which notifies when a customer subscription is deleted


@receiver(WEBHOOK_SIGNALS['customer.subscription.deleted'])
def subscription_deleted(sender, **kwargs):
    print('cancelled')


# funtion tied to the webhook which notifies when a customer subscription recurring payment fails
@receiver(WEBHOOK_SIGNALS['invoice.payment_failed'])
def subscription_payment_failed(sender, **kwargs):
    # get the stripe customer id whose subscription failed
    customer_id = kwargs['event'].data['object']['customer']

    # fetch the user profile of the customer and mark as non-member
    user_profile = UserProfile.objects.get(stripe_customer_id=customer_id)
    user_profile.is_member = False
    user_profile.save()

    # get the membership detail of the customer and update as membership_terminated_date as today
    membership_detail = MembershipDetail.objects.get(user=user_profile.user)
    membership_detail.date_terminated = datetime.date.today()
    membership_detail.save()


# load City names on select on Country in Membership Form
def load_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country__id=country_id)
    return JsonResponse(list(cities.values('id', 'name')), safe=False)
