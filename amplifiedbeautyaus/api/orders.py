from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from amplifiedbeautyaus.models import Order
from amplifiedbeautyaus.response import CommonResponse
from amplifiedbeautyaus.serializers.order import OrderSerializer


class GetOrderDetails(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, pk):
        try:
            order = self.queryset.get(id=pk)
            serializer = self.serializer_class(
                order,
                context={'request': request}
            )
            return CommonResponse(success=True, data=serializer.data)
        except:
            return CommonResponse(success=False, message="We couldn't find the Order that you're trying to find")


class GetAllPastOrders(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request):
        queryset = self.queryset.filter(
            customer=request.user.customer,
            status__in=[Order.SHIPPED]
        )
        serializer = self.serializer_class(
            queryset,
            many=True,
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)


class GetAllActiveOrders(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request):
        queryset = self.queryset.filter(
            customer=request.user.customer,
            status__in=[Order.ORDERED, Order.PREPARING]
        )
        serializer = self.serializer_class(
            queryset,
            many=True,
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)
