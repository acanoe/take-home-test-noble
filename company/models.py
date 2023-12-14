from django.db import models
from utils.abstract_models import UserTimestampedAbstract

class IndustryChoices(models.TextChoices):
    FINTECH = ('FINTECH', 'FINTECH')
    EDUTECH = ('EDUTECH', 'EDUTECH')
    ECOMMERCE = ('ECOMMERCE', 'ECOMMERCE')

class Company(UserTimestampedAbstract):
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=200, choices=IndustryChoices.choices)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'