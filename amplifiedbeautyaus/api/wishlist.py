from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from amplifiedbeautyaus.response import CommonResponse
from amplifiedbeautyaus.serializers import ProductSerializer, ProductWishlistSerializer


class GetCustomerWishlist(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def get(self, request):
        serializer = self.serializer_class(
            request.user.customer.wishlisted_products.all(),
            many=True,
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)


class AddProductToWishlist(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductWishlistSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            request.user.customer.wishlisted_products.add(serializer.validated_data['id'])
            return CommonResponse(success=True)
        return CommonResponse(success=False)


class RemoveProductFromWishlist(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductWishlistSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            request.user.customer.wishlisted_products.remove(serializer.validated_data['id'])
            return CommonResponse(success=True)
        return CommonResponse(success=False)
