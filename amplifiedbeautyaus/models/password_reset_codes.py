from random import choice
from string import digits

from django.db import models
from django_extensions.db.fields import CreationDateTimeField
from django.contrib.auth.models import User


def generate_code():
    return ''.join(choice(digits) for i in range(6))


class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default=generate_code)
    created = CreationDateTimeField()
    used = models.DateTimeField(null=True, blank=True, default=None)
