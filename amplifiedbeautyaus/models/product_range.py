from django.db import models


class ProductRange(models.Model):
    name = models.CharField(max_length=64, null=True, help_text="The name of this Product Range")
    image = models.ImageField(upload_to='product_ranges/', null=True, help_text="The Image for this Product Range")
    color = models.CharField(max_length=24, null=True, help_text="What color does this Range come in?")
    products = models.ManyToManyField('Product', blank=True)

    def __str__(self):
        return self.name
