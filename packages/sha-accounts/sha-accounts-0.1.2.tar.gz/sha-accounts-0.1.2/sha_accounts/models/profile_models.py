from django.db import models
from djrest_wrapper.interfaces import BaseModel


class AbstractProfile(BaseModel):
    class Meta:
        abstract = True


class Profile(AbstractProfile):
    user = models.OneToOneField('sha_accounts.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
