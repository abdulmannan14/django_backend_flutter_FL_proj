from decimal import Decimal

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from amplifiedbeautyaus.models import Cart, CartDetails, Product
from amplifiedbeautyaus.serializers import CartSerializer, AddToCartSerializer
from amplifiedbeautyaus.response import CommonResponse


class GetUserCart(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get(self, request):
        serializer = self.serializer_class(
            self.queryset.get_or_create(customer_id=request.user.customer.id)[0],
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)


class AddItemToCart(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AddToCartSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product = Product.objects.get(id=serializer.validated_data['id'])
            cart_detail = CartDetails.objects.create(
                cart=request.user.customer.cart,
                product_id=serializer.validated_data['id'],
                quantity=serializer.validated_data['quantity'],
                sub_total=product.price * serializer.validated_data['quantity'],
                item_notes=serializer.validated_data['item_notes'],
            )

            print(str(cart_detail.sub_total))

            request.user.customer.cart.sub_total += Decimal(cart_detail.sub_total)
            request.user.customer.cart.total += Decimal(cart_detail.sub_total)
            request.user.customer.cart.save(update_fields=['sub_total', 'total'])
            return CommonResponse(success=True)
        return CommonResponse(success=False, message="The data sent from your app version was invalid")


class RemoveItemFromCart(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = CartDetails.objects.all()
    serializer_class = CartSerializer

    def post(self, request, pk):
        # Get the Cart Item
        cart_item = self.queryset.get(id=pk)

        print(str(cart_item.sub_total))

        # Remove the cost from the Users Cart
        request.user.customer.cart.sub_total -= Decimal(cart_item.sub_total)
        request.user.customer.cart.total -= Decimal(cart_item.sub_total)
        request.user.customer.cart.save(update_fields=['sub_total', 'total'])

        # Delete the Cart Item
        cart_item.delete()

        # Serialize the Cart for the User and send it back to them on the app
        serializer = self.serializer_class(
            Cart.objects.get(customer_id=request.user.customer.id),
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)


class AddQuantityFromCart(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = CartDetails.objects.all()
    serializer_class = CartSerializer

    def post(self, request, pk):
        cart_item = self.queryset.get(id=pk)
        cart_item.quantity += 1
        cart_item.sub_total += Decimal(cart_item.product.price)
        cart_item.save(update_fields=['quantity', 'sub_total'])

        print(str(cart_item.product.price))

        request.user.customer.cart.sub_total += Decimal(cart_item.product.price)
        request.user.customer.cart.total += Decimal(cart_item.product.price)
        request.user.customer.cart.save(update_fields=['sub_total', 'total'])

        serializer = self.serializer_class(
            Cart.objects.get(customer_id=request.user.customer.id),
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)


class RemoveQuantityFromCart(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = CartDetails.objects.all()
    serializer_class = CartSerializer

    def post(self, request, pk):
        cart_item = self.queryset.get(id=pk)
        cart_item.quantity -= 1
        cart_item.sub_total -= Decimal(cart_item.product.price)
        cart_item.save(update_fields=['quantity', 'sub_total'])

        print(str(cart_item.product.price))

        request.user.customer.cart.sub_total -= Decimal(cart_item.product.price)
        request.user.customer.cart.total -= Decimal(cart_item.product.price)
        request.user.customer.cart.save(update_fields=['sub_total', 'total'])

        serializer = self.serializer_class(
            Cart.objects.get(customer_id=request.user.customer.id),
            context={'request': request}
        )
        return CommonResponse(success=True, data=serializer.data)
