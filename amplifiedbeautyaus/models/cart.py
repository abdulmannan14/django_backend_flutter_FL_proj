from django.db import models
from django.utils import timezone


class Cart(models.Model):
    customer = models.OneToOneField('Customer', on_delete=models.CASCADE, related_name='cart')
    address = models.ForeignKey('CustomerAddresses', on_delete=models.CASCADE, null=True, blank=True,
                                help_text="Delivery Address for this Order")
    sub_total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    delivery_fee = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Cart for: " + self.customer.first_name + " " + self.customer.last_name
