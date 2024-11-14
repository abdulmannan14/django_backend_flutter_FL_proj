from django.contrib.auth import get_user_model
from django.db import models

from amplifiedbeautyaus.sms_connector import send_sms

import stripe


class Customer(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,
                                help_text='The User assigned to this Customer')
    avatar = models.ImageField(upload_to='user_avatars/', default='blank.png', help_text="Customers Avatar Image")
    first_name = models.CharField(max_length=48, null=True, help_text='Customers First Name')
    last_name = models.CharField(max_length=64, null=True, help_text='Customers Last Name')
    phone = models.CharField(max_length=12, null=True, help_text="Customers Phone Number")
    email = models.CharField(max_length=128, null=True, help_text='Customers Email')
    stripe_user_id = models.CharField(max_length=128, null=True, help_text="Users Stripe ID")
    payment_card_id = models.CharField(max_length=128, null=True, help_text="Payment Card ID")
    bookmarked_tips = models.ManyToManyField('Tips', blank=True)
    wishlisted_products = models.ManyToManyField('Product', blank=True)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

    def send_sms_to_customer(self, message):
        send_sms(self.phone, message)

    def register_stripe_user(email, name, phone):
        stripe_customer = stripe.Customer.create(
            description="The b!te Network - Customer",
            name=name,
            email=email,
            phone=phone
        )
        return stripe_customer

    def register_card(self, token):
        try:
            card = stripe.Customer.create_source(
                "" + self.stripe_user_id,
                source=token
            )
            self.payment_card_id = card.id
            self.save()
            return card.id
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            print('Status is: %s' % e.http_status)
            print('Code is: %s' % e.code)
            # param is '' in this case
            print('Param is: %s' % e.param)
            print('Message is: %s' % e.user_message)
            return False
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            print(e)
            return False
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print(e)
            return False
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            print(e)
            return False
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            print(e)
            return False
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            print(e)
            return False
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            print(e)
            return False

    def check_card_details(self):
        try:
            card = stripe.Customer.retrieve_source(
                self.stripe_user_id,
                self.payment_card_id
            )
            self.card_country = card['country']
            self.save()
            return card
        except Exception as e:
            print(e)
            return False
    

class CustomerAddresses(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, related_name="addresses",
                                 help_text="The Customer that created this delivery address")
    address = models.CharField(max_length=1024, null=True, help_text="Delivery Address")
    default = models.BooleanField(default=False)
