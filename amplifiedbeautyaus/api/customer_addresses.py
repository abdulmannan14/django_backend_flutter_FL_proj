from decimal import Decimal

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from amplifiedbeautyaus.models import Cart, CustomerAddresses
from amplifiedbeautyaus.serializers import CustomerAddressSerializer, CustomerSetAddressSerializer, \
    CustomerCreateAddressSerializer
from amplifiedbeautyaus.response import CommonResponse


class GetCustomerAddresses(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerAddressSerializer

    def get(self, request):
        serializer = self.serializer_class(
            request.user.customer.addresses.all(),
            many=True,
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)


class SetCustomerAddress(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CustomerSetAddressSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            cart = self.queryset.get(customer_id=request.user.customer.id)
            address = None
            try:
                address = CustomerAddresses.objects.get(customer=request.user.customer,
                                                        address__icontains=serializer.validated_data['address'])
            except CustomerAddresses.MultipleObjectsReturned:
                address = CustomerAddresses.objects.filter(customer=request.user.customer,
                                                           address__icontains=serializer.
                                                           validated_data['address']).first()
            except CustomerAddresses.DoesNotExist:
                address = CustomerAddresses.objects.create(
                    customer=request.user.customer,
                    address=serializer.validated_data['address']
                )

            single_item_delivery = Decimal(9.00)
            # express_item_delivery = Decimal(15.00)

            # if not cart.address and cart.cart_details.all().count() == 1:
            cart.delivery_fee = single_item_delivery
            cart.total += cart.delivery_fee
            # elif not cart.address and cart.cart_details.all().count() > 1:
            #     cart.delivery_fee = express_item_delivery
            #     cart.total += express_item_delivery

            cart.address = address
            cart.save(update_fields=['address', 'delivery_fee', 'total'])
            return CommonResponse(success=True)
        return CommonResponse(success=False, message="The Data returned from your App was Invalid")


class CreateCustomerAddress(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerCreateAddressSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            request.user.customer.addresses.create(
                address=serializer.validated_data['address'],
                default=True,
            )
            return CommonResponse(success=True)
        return CommonResponse(success=False, message="The Data sent from your app version is invalid")


class DeleteCustomerAddress(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerCreateAddressSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            address = CustomerAddresses.objects.filter(
                customer=request.user.customer,
                address=serializer.validated_data['address']
            )
            address.delete()
            return CommonResponse(success=True, message="Deleted Delivery Address")
        return CommonResponse(success=False, message="The Data sent from your app version is invalid")
