from django.contrib.auth.models import AbstractUser
from django.db import models

status_choices = [("DEFAULT", "default"), ("VIP" ,"vip")]

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    status = models.CharField(max_length=15, choices=status_choices, default="DEFAULT")

    def __str__(self):
        return self.username
