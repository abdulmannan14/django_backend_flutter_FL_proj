from django.db import models


class ProductReviews(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, help_text="User that gave the review")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, help_text="Product associated to Review",
                                related_name="product_review")
    rating = models.DecimalField(max_digits=4, decimal_places=2, help_text="Rating given to this Product?")
    review = models.CharField(max_length=256, null=True, help_text="Rating for this Product")
    date_added = models.DateTimeField(auto_now_add=True, null=True, help_text="Date this review was added")
