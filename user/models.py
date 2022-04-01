from django.db import models
from core.models import Template

class User(Template, models.Model):
    phone_number = models.TextField(max_length=255)
