from colorfield.fields import ColorField
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=64, null=True, help_text="Name of this Product")
    product_range = models.ForeignKey('ProductRange', on_delete=models.CASCADE, default="1", null=True, blank=True,
                                      help_text="Product Range for this Product")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text="Product Price")
    description = models.TextField(max_length=512, null=True, help_text="Description for this Product")

    duration = models.CharField(max_length=16, null=True, help_text="How long does this product last for?")
    fragrance = models.CharField(max_length=16, null=True, help_text="What does this product smell like?")
    type = models.CharField(max_length=16, null=True, help_text="What type of product is this?")
    color = ColorField(default="FF0000", null=True, help_text="What is the color of this product?")

    estimated_timeframe = models.CharField(max_length=16, null=True, help_text="How long will it take to be delivered?")

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, help_text="Product for this Image",
                                related_name='product_images')
    image = models.ImageField(upload_to='product_images/', null=True, help_text="Image for this Product")
