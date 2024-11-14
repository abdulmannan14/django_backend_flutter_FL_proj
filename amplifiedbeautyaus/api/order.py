import stripe
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from amplifiedbeautyaus.models import Order, OrderDetails, UserAlert
from amplifiedbeautyaus.response import CommonResponse


class PlaceOrderView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            cart = request.user.customer.cart
        except:
            return CommonResponse(success=False, message="We couldn't find your Cart for todays order. "
                                                         "Please reload the ABA App and try again")

        print(cart)
        print(cart.address)
        if cart.address is None:
            return CommonResponse(success=False, message="We require a valid delivery address to send your order to")

        order = Order.objects.create(
            customer=request.user.customer,
            address=cart.address,
            sub_total=cart.sub_total,
            delivery_fee=cart.delivery_fee,
            total=cart.total
        )

        for item in cart.cart_details.all():
            print(order)
            print(item.product.name)
            print(item.quantity)
            print(item.sub_total)
            print(item.item_notes)
            OrderDetails.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                sub_total=item.sub_total,
                item_notes=item.item_notes,
            )
        cart.delete()

        # TODO: CREATE AN ALERT FOR THE CUSTOMER
        UserAlert.objects.create(
            user=request.user.customer,
            text="Order #{number} with Amplified Beauty Australia has been placed".format(number=str(order.id))
        )

        # TODO: SEND AN EMAIL TO ADMIN ABOUT NEW ORDER

        return CommonResponse(success=True, data={'id': order.id})
