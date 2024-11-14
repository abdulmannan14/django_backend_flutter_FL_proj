from django.db import models


class CartDetails(models.Model):
    cart = models.ForeignKey('Cart', related_name='cart_details', blank=True, default="1", on_delete=models.CASCADE)
    product = models.ForeignKey('Product', blank=True, default="1", on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, default="1")
    sub_total = models.DecimalField(decimal_places=2, max_digits=10, default="1")
    item_notes = models.CharField(max_length=500, blank=True, null=True)
