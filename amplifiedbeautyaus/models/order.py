from django.db import models
from django.utils import timezone
from django_random_id_model import RandomIDModel


class Order(RandomIDModel):
    ORDERED = 1
    PREPARING = 2
    SHIPPED = 3

    ORDER_STATUSES = (
        (ORDERED, "Order Placed"),
        (PREPARING, "Preparing your Order"),
        (SHIPPED, "Order Shipped"),
    )

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='order_customer')
    address = models.ForeignKey('CustomerAddresses', on_delete=models.CASCADE, null=True, blank=True,
                                help_text="Delivery Address for this Order")
    status = models.IntegerField(choices=ORDER_STATUSES, default=1)
    sub_total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    delivery_fee = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    total = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(default=timezone.now)


class OrderDetails(models.Model):
    order = models.ForeignKey('Order', related_name='order_details', blank=True, default="1", on_delete=models.CASCADE)
    product = models.ForeignKey('Product', blank=True, default="1", on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, default="1")
    sub_total = models.DecimalField(decimal_places=2, max_digits=10, default="1")
    item_notes = models.CharField(max_length=500, blank=True, null=True)
