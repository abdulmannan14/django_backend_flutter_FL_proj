import phonenumbers

from django.conf import settings

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def send_sms(number, message, fail_silently=True):
    # logger = logging.getLogger('tca.sms')

    # Format the number in International Format
    formatted_number = phonenumbers.format_number(phonenumbers.parse(number, settings.PHONE_NUMBER_COUNTRY),
                                                  phonenumbers.PhoneNumberFormat.E164)

    # logger.debug(f'SMS to {formatted_number}: {Truncator(message).chars(100)}')

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(from_=settings.TWILIO_NUMBER, to=formatted_number, body=message)
        # logger.debug(f'Message ID: {message.sid}')
    except TwilioRestException as error:
        if not fail_silently:
            raise
