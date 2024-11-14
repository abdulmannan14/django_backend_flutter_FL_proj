from django.db import models


class Tips(models.Model):
    name = models.CharField(max_length=64, null=True, help_text="The name for this Tip")
    image = models.ImageField(upload_to='tips/', null=True, help_text="The Image for this Tip")
    content = models.TextField(max_length=1024, null=True, help_text="The Text to show inside this Tip")
    