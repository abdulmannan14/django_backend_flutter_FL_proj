from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from amplifiedbeautyaus.models import Tips
from amplifiedbeautyaus.serializers import TipsSerializer
from amplifiedbeautyaus.response import CommonResponse


class GetAllTipsView(APIView):
    queryset = Tips.objects.all()
    serializer_class = TipsSerializer

    def get(self, request):
        serializer = self.serializer_class(
            self.queryset.all(),
            many=True,
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)


class GetBookmarkedTipsView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tips.objects.all()
    serializer_class = TipsSerializer

    def get(self, request):
        serializer = self.serializer_class(
            request.user.customer.bookmarked_tips.all(),
            many=True,
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)


class AddBookmarkTipView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tips.objects.all()
    serializer_class = TipsSerializer

    def post(self, request, pk):
        queryset = self.queryset.get(id=pk)
        request.user.customer.bookmarked_tips.add(queryset)
        serializer = self.serializer_class(
            queryset,
            context={'request': request}
        )
        return CommonResponse(success=True, message="Tip Added to your Bookmarks", data=serializer.data)


class RemoveBookmarkTipView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tips.objects.all()
    serializer_class = TipsSerializer

    def post(self, request, pk):
        queryset = self.queryset.get(id=pk)
        request.user.customer.bookmarked_tips.remove(queryset)
        serializer = self.serializer_class(
            queryset,
            context={'request': request}
        )
        return CommonResponse(success=True, message="Tip Removed from your Bookmarks", data=serializer.data)