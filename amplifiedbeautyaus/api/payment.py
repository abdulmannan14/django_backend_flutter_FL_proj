import stripe
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from amplifiedbeautyaus.models import Cart
from amplifiedbeautyaus.response import CommonResponse
from amplifiedbeautyaus.serializers import UpdatePaymentSerializer


class UpdatePaymentMethodView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Get the Users Cart
        cart = Cart.objects.get_or_create(customer_id=request.user.customer.id)[0]

        # Create the Ephemeral Key
        key = stripe.EphemeralKey.create(
            customer=request.user.customer.stripe_user_id,
            stripe_version='2020-08-27'
        )

        # Create the Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(cart.total * 100),
            currency='aud',
            capture_method='manual',
            description="Amplified Beauty Aus",
            statement_descriptor="Amplified Beauty Aus",
            confirm=False,
            customer=request.user.customer.stripe_user_id,
            payment_method_types=[
                'card',
            ],
        )

        return CommonResponse(
            success=True,
            message="Generated Payment Intent Token for Payment Sheet",
            data={
                  "intent": payment_intent.id,
                  "intent_secret": payment_intent.client_secret,
                  "ephemeral": key.secret,
                  "customer": request.user.customer.stripe_user_id
              }
        )
