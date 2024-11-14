from django.db import models


class UserAlert(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, help_text="Customer that received this Notification")
    text = models.CharField(max_length=256, null=True, help_text="Text for this Notification")
    timestamp = models.DateTimeField(auto_now=True, help_text="The Time and Date this Notification was received")
