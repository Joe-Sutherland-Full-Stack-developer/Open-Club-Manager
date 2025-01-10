from django.apps import apps
from django.conf import settings

from django.apps import apps
import stripe

def get_stripe_keys():
    # Get the StripeIntegration model
    StripeIntegration = apps.get_model('dashboard', 'StripeIntegration')
    
    # Retrieve the first instance of StripeIntegration
    stripe_keys = StripeIntegration.objects.first()
    
    # Return the publishable and secret keys if available, otherwise return None
    if stripe_keys:
        return stripe_keys.stripe_publishable_key, stripe_keys.stripe_secret_key
    return None, None

def initialize_stripe():
    # Get the publishable and secret keys
    publishable_key, secret_key = get_stripe_keys()
    
    if secret_key:
        # Set the Stripe API key globally
        stripe.api_key = secret_key  # Correctly set the global api_key
    
    return publishable_key  # Return the publishable key for frontend use

def get_stripe_secret_key():
    # Get the StripeIntegration model
    StripeIntegration = apps.get_model('dashboard', 'StripeIntegration')
    
    # Retrieve the first instance of StripeIntegration
    stripe_keys = StripeIntegration.objects.first()
    
    # Return the secret key if available, otherwise return None
    if stripe_keys:
        return stripe_keys.stripe_secret_key
    
    return None


