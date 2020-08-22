from django import template
import stripe
register = template.Library()

# To get the price details of the Stripe price
@register.filter
def get_stripe_price_details(stripe_price_id):
	price = stripe.Price.retrieve(stripe_price_id)
	return price['unit_amount']/100


@register.filter
def get_stripe_subscription_amount(stripe_subscription_id):
	subscription=stripe.Subscription.retrieve(stripe_subscription_id)
	return subscription['items']['data'][0]['price']['unit_amount']/100


@register.filter
def get_stripe_subscription_interval(stripe_subscription_id):
	subscription=stripe.Subscription.retrieve(stripe_subscription_id)
	return subscription['items']['data'][0]['price']['recurring']['interval']



	


@register.simple_tag
def define(val=None):
	return val


