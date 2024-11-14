from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from amplifiedbeautyaus.serializers import CustomerSerializer
from amplifiedbeautyaus.response import CommonResponse


class GetCustomerProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer

    def get(self, request):
        serializer = self.serializer_class(
            request.user.customer,
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)


