from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from requests.exceptions import HTTPError
from social_core.backends.google import GoogleOAuth2

from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden

from amplifiedbeautyaus.models import Customer
from amplifiedbeautyaus.response import CommonResponse
from amplifiedbeautyaus.serializers import AppleLoginSerializer


class GoogleLoginView(generics.GenericAPIView):
    """Sign in with Google"""
    serializer_class = AppleLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        oauth_provider = GoogleOAuth2()
        print(serializer.validated_data)

        try:
            access_token = serializer.data.get('access_token')
            user = oauth_provider.do_auth(access_token=access_token)
            print(user)
        except HTTPError as error:
            return CommonResponse(success=False, message=str(error))
        except AuthTokenError as error:
            return CommonResponse(success=False, message=str(error))

        if user:
            # Generated a DRF Token for this User
            user = User.objects.filter(username=user).first()
            customer_exists = Customer.objects.filter(user__username=user).exists()
            print(customer_exists)
            if not customer_exists:
                returned_data = {
                    'data_required': True,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
                return CommonResponse(success=True,
                                      message="We need some more data from you to setup your Amplified Beauty account. "
                                              "Please enter the information on the next page to use Amplified Beauty",
                                      data=returned_data)
            customer = Customer.objects.filter(email=user.email).first()
            token = Token.objects.get_or_create(user=customer.user)[0]
            response = {
                'data_required': False,
                'email': user.email,
                'id': customer.user.id,
                'username': customer.user.username,
                'token': token.key,
            }
            return CommonResponse(success=True, data=response)
        return CommonResponse(success=True, message="We couldn't log you in at this moment")
