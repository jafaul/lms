from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

User = get_user_model()

# class User(models.Model):
#     email = models.EmailField(unique=True, max_length=36)
#     password = models.CharField(max_length=36)
#     name = models.CharField(_('Name'), max_length=36)
#     surname = models.CharField(_('Surname'), max_length=40)
#     photo = models.ImageField(_('Photo'), upload_to='users/%Y/%m/%d', null=True, blank=True)
#     phone_number = models.CharField(max_length=20, blank=True, null=True)
#
#     def __str__(self):
#         return self.name + " " + self.surname