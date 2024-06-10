from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
class User(AbstractUser):
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='updated_users', null=True, blank=True)
    email2 = models.EmailField(db_index=True, null=True, blank=True, unique=True)
    phone = models.CharField(validators=[phone_regex], max_length=15, null=True, blank=True, unique=True)
    phone2 = models.CharField(validators=[phone_regex], max_length=15, null=True, blank=True, unique=True)

    