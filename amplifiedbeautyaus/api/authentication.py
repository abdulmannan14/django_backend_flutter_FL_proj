from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token

from amplifiedbeautyaus.models import Customer, Cart
from amplifiedbeautyaus.serializers import LoginSerializer, CustomerRegisterSerializer
from amplifiedbeautyaus.response import CommonResponse


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
            if user is None:
                return CommonResponse(success=False, message='Incorrect username or password.')

            token = Token.objects.get_or_create(user=user)[0]
            return CommonResponse(data={
                'token': token.key,
                'username': user.username,
                'id': user.id,
            })
            return CommonResponse(success=True, message="Logged in Successfully")
        return CommonResponse(success=False, message="Invalid Username or Password")


class CustomerRegisterView(APIView):
    permission_classes = ()
    serializer_class = CustomerRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data['first_name'])
            print(serializer.validated_data['last_name'])
            print(serializer.validated_data['email'])
            print(serializer.validated_data['password'])
            print(serializer.validated_data['phone'])

            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                print(user.username)
                print(user.first_name)
                user.set_password(raw_password=serializer.validated_data['password'])
                user.save()
            except IntegrityError:
                return CommonResponse(success=False, message="An Account with that Email Address already exists. "
                                                             "If you've logged into our app before, "
                                                             "please use your Email Address to login")
            except:
                user = User.objects.create_user(
                    username=serializer.validated_data['email'],
                    password=serializer.validated_data['password'],
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name'],
                    email=serializer.validated_data['email'],
                )

            stripe_user = Customer.register_stripe_user(serializer.validated_data['email'],
                                                        serializer.validated_data['first_name'],
                                                        serializer.validated_data['phone'])

            try:
                customer = Customer.objects.create(
                    user=user,
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name'],
                    email=serializer.validated_data['email'],
                    phone=serializer.validated_data['phone'],
                    stripe_user_id=stripe_user.id,
                )
            except IntegrityError:
                return CommonResponse(success=False, message="An Account with that Email Address already exists. "
                                                             "If you've logged into our app before, "
                                                             "please use your Email Address to login")

            Cart.objects.create(
                customer=customer,
                total=0.00,
            )

            # try:
            print(user.username)
            print(serializer.validated_data['password'])
            user_login = authenticate(username=customer.user,
                                      password=serializer.validated_data['password'])
            print(user_login)
            if user_login is None:
                return CommonResponse(success=False, message='Incorrect username or password.')

            token = Token.objects.get_or_create(user=user_login)[0]

            return CommonResponse(data={
                'token': token.key,
                'username': user_login.username,
                'id': user_login.id,
            })
            # except:
            #     pass
            return CommonResponse(success=True, message="You're Registered 🎉 Let's Login and Get Ordering!")
        return CommonResponse(success=False, message="Data is missing from your request")
