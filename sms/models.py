from random import choices
from django.db import models
from core.models import Template
from user.models import User


class SmsClass(models.Model):
    CLASS_CHOICES = {
        (1, 'Personal'),
        (2, 'Advertisement'),
        (3, 'Fraud'),
    }

    type = models.IntegerField(choices = CLASS_CHOICES) 


class Sms(Template, models.Model):
    sender = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='sender')
    recipient = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='recipient')
    message = models.TextField(null=True, blank=True)
    type = models.ForeignKey(SmsClass, on_delete=models.CASCADE)
