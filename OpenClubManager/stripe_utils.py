from django.apps import apps
import stripe


def get_stripe_keys():
    StripeIntegration = apps.get_model('dashboard', 'StripeIntegration')
    stripe_keys = StripeIntegration.objects.first()

    if stripe_keys:
        return (
            stripe_keys.stripe_publishable_key,
            stripe_keys.stripe_secret_key
        )
    return None, None


def initialize_stripe():
    publishable_key, secret_key = get_stripe_keys()

    if secret_key:
        stripe.api_key = secret_key

    return publishable_key


def get_stripe_secret_key():
    StripeIntegration = apps.get_model('dashboard', 'StripeIntegration')
    stripe_keys = StripeIntegration.objects.first()

    if stripe_keys:
        return stripe_keys.stripe_secret_key

    return None
