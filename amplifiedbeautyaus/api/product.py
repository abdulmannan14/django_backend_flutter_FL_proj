from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from amplifiedbeautyaus.serializers import ProductSerializer
from amplifiedbeautyaus.models import Product
from amplifiedbeautyaus.response import CommonResponse


class GetPopularProductsView(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request):
        queryset = self.queryset.all().order_by('?')
        serializer = self.serializer_class(
            queryset,
            many=True,
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)


class GetProductDetail(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk):
        queryset = self.queryset.get(id=pk)
        serializer = self.serializer_class(
            queryset,
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)


class SearchProducts(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, query):
        queryset = self.queryset.filter(name__icontains=query)
        serializer = self.serializer_class(
            queryset,
            many=True,
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)
