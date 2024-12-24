from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class OTP(models.Model):
    token = models.CharField(max_length=255, unique=True)
    mobile = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mobile

    def is_valid(self):
        # save code with 5 min 
        return now() < self.created_at + timedelta(minutes=5)


class FailedLoginAttempt(models.Model):
    ip_address = models.GenericIPAddressField()
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ip_address


