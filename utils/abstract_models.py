from django.db import models
from user.models import User
from company.models import Company

class TimestampedAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class UserTimestampedAbstract(TimestampedAbstract):
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_updated_by', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created_by')
    
    class Meta:
        abstract=True

class CompanyOwnershipAbstract(UserTimestampedAbstract):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='%(class)s_entities')
    
    class Meta:
        abstract=True