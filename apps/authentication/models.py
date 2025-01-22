from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

# User = get_user_model()

# class UserData(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

class SchoolUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField(_('email address'), unique=True)
    objects = SchoolUserManager()

#
# # https://docs.djangoproject.com/en/5.1/topics/auth/customizing/
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
