from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from .forms import MembershipDetailForm, DonationForm
from django.conf import settings
from .models import *
from django.contrib import messages
from django.contrib.auth.models import Group
from django.views.generic import View
from django.contrib.auth.decorators import login_required
import stripe
import datetime
stripe.api_key = settings.STRIPE_KEY


def create_donation(request):
    print('POST==', request.POST)
    if 'amount' in request.session:
        amount = int(request.session['amount'])*100
    stripe.Charge.create(
        amount=amount,
        source=request.POST['stripeToken'],
        currency="inr",
        description="===Donation===",
    )
    messages.success(request, 'Your donation has been received !')
    return redirect(reverse('thankyou'))


def chargeCustomer(request):
    print('======chargeCustomer============')
    customer = stripe.Customer.create(
        email=request.POST['email'], name=request.POST['name'], source=request.POST['stripeToken'])

    user_membership_detail = MembershipDetail.objects.get(user=request.user)
    user_membership_detail.stripe_customer_id = customer.id
    user_membership_type = user_membership_detail.membership_type
    if user_membership_detail.membership_term == 'M':
        price_id = user_membership_type.stripe_monthly_price_id
        amount = user_membership_type.monthly_price
        description = user_membership_type.type_name + ' Monthly Plan Payment'

    elif user_membership_detail.membership_term == 'Y':
        price_id = user_membership_type.stripe_yearly_price_id
        amount = user_membership_type.yearly_price_after_discount
        description = user_membership_type.type_name + ' Yearly Plan Payment'

    stripe.Subscription.create(
        customer=customer.id,
        items=[
            {"price": price_id},
        ],
    )
    user_membership_detail.is_paid_up = True
    user_membership_detail.date_joined = datetime.date.today()
    user_membership_detail.save()

    user_payment_history = MemberPaymentHistory()
    user_payment_history.user = request.user
    user_payment_history.amount = amount
    user_payment_history.description = description
    user_payment_history.save()

    group = Group.objects.get(name=user_membership_type.membership_group)
    group.user_set.add(request.user)

    messages.success(request, 'Your membership has been activated !')
    return redirect(reverse('thankyou'))


# def create_subscription(request,customer,price):
#     import stripe
# stripe.api_key = "sk_test_51H4o50DLCEyNZL8YOpFgmi8jI0sWDslQ9GRkPZ12SqkglAkJiidioJGvV0MV0vEYNLVF7Mqd9qbvEhOEDyDslxzg00L3V56wUF"

# stripe.Subscription.create(
#   customer="cus_HiqdXrJnNK61rk",
#   items=[
#     {"price": "price_1H9O8fDLCEyNZL8Y3wigPeIF"},
#   ],
# )


# def create_product(requ)


# def create_membership


#     import stripe
# stripe.api_key = "sk_test_51H4o50DLCEyNZL8YOpFgmi8jI0sWDslQ9GRkPZ12SqkglAkJiidioJGvV0MV0vEYNLVF7Mqd9qbvEhOEDyDslxzg00L3V56wUF"

# stripe.Subscription.create(
#   customer="cus_Hiq6dx4oGJKpRT",
#   items=[
#     {"price": "price_1H9O8fDLCEyNZL8Y3wigPeIF"},
#   ],
# )


# import stripe
# stripe.api_key = "sk_test_51H4o50DLCEyNZL8YOpFgmi8jI0sWDslQ9GRkPZ12SqkglAkJiidioJGvV0MV0vEYNLVF7Mqd9qbvEhOEDyDslxzg00L3V56wUF"

# stripe.Customer.retrieve("cus_Hiq9Jcoa0fYaz9")


# import stripe
# stripe.api_key = "sk_test_51H4o50DLCEyNZL8YOpFgmi8jI0sWDslQ9GRkPZ12SqkglAkJiidioJGvV0MV0vEYNLVF7Mqd9qbvEhOEDyDslxzg00L3V56wUF"

# stripe.Price.create(
#   unit_amount=100000,
#   currency="inr",
#   recurring={"interval": "year"},
#   product="prod_HipoYTBL8x0S0w",
# )


# import stripe
# stripe.api_key = "sk_test_51H4o50DLCEyNZL8YOpFgmi8jI0sWDslQ9GRkPZ12SqkglAkJiidioJGvV0MV0vEYNLVF7Mqd9qbvEhOEDyDslxzg00L3V56wUF"

# stripe.Product.create(name="Gold Special")


def stripee_create_membership(request):
    return render(request, 'stripee_create_membership.html')


def payment_history(request):
    
    return render(request, 'payment_history.html')



def stripee_create_donation(request):
    return render(request, 'stripee_create_donation.html')


# class StripeView(View):

#     def get(self,*args, **kwargs):
#         print(self.request.GET)
#         context = {'payment_type':'membership'}
#         return render(self.request, 'stripee.html', context)

#     def post(self,*args, **kwargs):
#         print(self.request.POST)
#         print('payment_type ==',self.request.POST.get('payment_type'))
#         if self.request.POST.get('payment_type') == 'membership':
#             return redirect('create_membership')
#         elif self.request.POST.get('payment_type') == 'donation':
#             return redirect('create_donation')


def stripee_two(request):
    return render(request, 'stripee_two.html')


@login_required
def membership(request):

    if request.method == 'POST':
        form = MembershipDetailForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.first_name = request.user.first_name
            instance.last_name = request.user.last_name
            if form.cleaned_data.get('city') != '':
                city = City()
                city.name = form.cleaned_data.get('city')
                city.save()
                instance.city_id = city

            instance.save()
            request.session['payment_type'] = 'membership'
            # request.session['amount'] = get_membership_amount(
            #     instance.membership_type, instance.membership_term)

            return redirect('stripee_create_membership')
            # if not request.GET._mutable:
            #     request.GET._mutable = True
            # request.GET['payment_type'] = 'membership'
            # print('GET=========',request.GET)
            # context = {'payment_type':'membership'}
            # return redirect(reverse('stripee',kwargs={'payment_type':'membership'}))
            # redirect(reverse('url_to_redirect_to', kwargs={'args_1':value}))
        else:
            print('invalid')
            # instance = form.save()
            context = {'form': form}
            return render(request, 'membership.html', context)

    # initial = {
    #     'first_name': request.user.first_name,
    #     'email': request.user.email}
    # first_name = request.user.first_name
    # last_name = request.user.last_name
    # form = JournalForm(initial={'tank': 123})
    # print('first = ',request.user.first_name)
    # print('last = ',request.user.last_name)
    # if not request.GET._mutable:
    #     request.GET._mutable = True
    # request.GET['payment_type'] = 'membership'
    # print('GET=========', request.GET)
    form_intial_values = {
        'first_name': request.user.first_name, 'last_name': request.user.last_name}
    form = MembershipDetailForm(initial=form_intial_values)
    context = {'form': form}
    return render(request, 'membership.html', context)


def donation(request):
    if request.method == 'POST':
        print('7')
        form = DonationForm(request.POST)
        if form.is_valid():
            print('form =', form.cleaned_data)
            instance = form.save()
            request.session['payment_type'] = 'donation'
            request.session['amount'] = form.cleaned_data.get('amount')
            request.session['payment_frequency'] = form.cleaned_data.get(
                'payment_frequency')
            return redirect('stripee_create_donation')
    form = DonationForm()
    donations = Donation.objects.all().count()
    context = {'form': form, 'donations': donations}

    return render(request, 'donation.html', context)

# def get_membership_amount(membership_type, membership_term):
#     print('in get_membership_amount')
#     if membership_term == 'M':
#         return membership_type.monthly_price
#     elif membership_term == 'Y':
#         return membership_type.yearly_price_after_discount
