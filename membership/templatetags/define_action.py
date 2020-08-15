from django import template
import stripe
register = template.Library()

# To get the price details of the Stripe price
@register.filter
def get_stripe_price_details(stripe_price_id):
    price = stripe.Price.retrieve(stripe_price_id)
    return price['unit_amount']/100


@register.simple_tag
def define(val=None):
    return val