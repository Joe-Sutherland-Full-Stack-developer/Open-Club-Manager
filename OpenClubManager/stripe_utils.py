from django.apps import apps
from django.conf import settings

def get_stripe_keys():
    StripeIntegration = apps.get_model('dashboard', 'StripeIntegration')
    stripe_keys = StripeIntegration.objects.first()
    if stripe_keys:
        return stripe_keys.stripe_publishable_key, stripe_keys.stripe_secret_key
    return None, None

def initialize_stripe():
    from stripe import api_key
    publishable_key, secret_key = get_stripe_keys()
    if secret_key:
        api_key = secret_key
    return publishable_key
