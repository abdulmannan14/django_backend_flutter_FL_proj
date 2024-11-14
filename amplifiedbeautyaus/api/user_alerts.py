from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from amplifiedbeautyaus.models import UserAlert
from amplifiedbeautyaus.serializers import UserAlertSerializer
from amplifiedbeautyaus.response import CommonResponse


class GetUserAlerts(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserAlert.objects.all()
    serializer_class = UserAlertSerializer

    def get(self, request):
        queryset = self.queryset.filter(user=request.user.customer)
        serializer = self.serializer_class(
            queryset,
            many=True,
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)


class DeleteUserAlert(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserAlert.objects.all()

    def post(self, request, pk):
        queryset = self.queryset.filter(id=pk)
        queryset.delete()
        return CommonResponse(success=True)


class DeleteAllUserAlerts(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserAlert.objects.all()

    def post(self, request):
        queryset = self.queryset.filter(user=request.user.customer)
        queryset.delete()
        return CommonResponse(success=True)
