from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.conf import settings

from amplifiedbeautyaus.serializers import RequestPasswordResetSerializer, ConfirmPasswordResetSerializer
from amplifiedbeautyaus.models import Customer, PasswordResetCode
from amplifiedbeautyaus.response import CommonResponse
from amplifiedbeautyaus.lang.sms import PASSWORD_RESET_CODE, PASSWORD_RESET_SUCCESS


class ResetPasswordRequestView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = RequestPasswordResetSerializer

    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                self.user = Customer.objects.get(phone=serializer.validated_data['phone'])
                print(self.user)
            except Customer.DoesNotExist:
                return CommonResponse(success=False, message="We cannot find an account on Amplified Beauty "
                                                             "Australia with that Mobile Number")
            except Customer.MultipleObjectsReturned:
                return CommonResponse(success=False, message="Unable to find an account with that Phone Number. "
                                                             "Multiple")

            print("STARTING RESET CODE")
            reset_code = PasswordResetCode.objects.create(user_id=self.user.user.id)
            reset_code.save()
            print("WORKING AT RESET CODE")
            self.reset_code = reset_code

            self.user.send_sms_to_customer(PASSWORD_RESET_CODE.format(code=reset_code.code))

            ph_tail = None
            if self.reset_code.user.customer.phone is not None:
                ph_str = str(self.reset_code.user.customer.phone)
                ph_tail = ph_str[-3:].rjust(len(ph_str) - 3, '*')
                return CommonResponse(success=True, data={'id': self.reset_code.id, 'ph_tail': ph_tail})
            return CommonResponse(success=False, message="We couldn't request a Password Reset for this account")
        return CommonResponse(success=False, message="We couldn't request a Password Reset for this account")


class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = ConfirmPasswordResetSerializer

    reset_code = None

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                time_threshold = timezone.now() - settings.PASSWORD_RESET_CODE_EXPIRY
                self.reset_code = PasswordResetCode.objects.get(id=serializer.validated_data['id'],
                                                                code=serializer.validated_data['code'],
                                                                created__gte=time_threshold, used__isnull=True)
            except PasswordResetCode.DoesNotExist:
                return CommonResponse(success=False,
                                      message="Unable to reset password - Please check the password reset code. "
                                      "Note that reset codes expire after 5 minutes.")

            self.reset_code.user.set_password(serializer.validated_data['password'])
            self.reset_code.user.save()

            self.reset_code.used = timezone.now()
            self.reset_code.save(update_fields=['used'])

            self.reset_code.user.customer.send_sms_to_customer(PASSWORD_RESET_SUCCESS)
            return CommonResponse(success=True, message="Password Successfully Reset. Please Login to Continue!")
        return CommonResponse(success=False, message="Unable to reset password. Please Check the Password Reset Code")
