from django.db import models
from django.contrib.auth.models import AbstractUser

class UserTypeChoices(models.TextChoices):
    OWNER = ('OWNER', 'OWNER')
    EMPLOYEE = ('EMPLOYEE', 'EMPLOYEE')

class User(AbstractUser):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='employee', null=True, blank=True)