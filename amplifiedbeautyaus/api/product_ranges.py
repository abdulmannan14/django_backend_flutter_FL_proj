from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from amplifiedbeautyaus.models import ProductRange
from amplifiedbeautyaus.serializers import ProductRangeSerializer
from amplifiedbeautyaus.response import CommonResponse


class GetProductRanges(APIView):
    serializer_class = ProductRangeSerializer

    def get(self, request):
        serializer = self.serializer_class(
            ProductRange.objects.all().order_by('?'),
            many=True,
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)


class GetProductRangeDetails(APIView):
    serializer_class = ProductRangeSerializer

    def get(self, request, pk):
        serializer = self.serializer_class(
            ProductRange.objects.get(id=pk),
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)


class GetProductRangeProducts(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductRangeSerializer

    def get(self, request, pk):
        serializer = self.serializer_class(
            ProductRange.objects.get(id=pk),
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)
