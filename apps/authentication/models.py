import os

import boto3
from botocore.exceptions import ClientError
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from storages.backends.s3boto3 import S3Boto3Storage

from config.settings import base
from config.settings.base import AWS_STORAGE_BUCKET_NAME


class SchoolUserManager(BaseUserManager):
    def create_user(self, email,  password=None, **extra_fields):
        # if not username:
        #     raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('position', User.Position.ADMIN)

        user = self.create_user(email, password, **extra_fields)

        admin_group, created = Group.objects.get_or_create(name="Admin")
        user.groups.add(admin_group)

        all_permissions = Permission.objects.all()
        admin_group.permissions.set(all_permissions)

        return user


class User(AbstractUser):
    class Position(models.TextChoices):
        ADMIN = "admin", _("Admin")
        MANAGER = "manager", _("Manager")
        TEACHER = "teacher", _("Teacher")
        STUDENT = "student", _("Student")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(_('email address'), unique=True)
    objects = SchoolUserManager()
    position = models.CharField(max_length=20, choices=Position.choices, default=Position.STUDENT)
    photo = models.ImageField(_("Photo"), null=True, blank=True, upload_to='photos/%Y/%m/%d', storage=S3Boto3Storage())

    def get_role_permissions(self):
        if self.position == self.Position.ADMIN:
            return Permission.objects.all()
        elif self.position == self.Position.MANAGER:
            return Permission.objects.filter(Q(codename__endswith="_lecture")|Q(codename="view_course"))
        return Permission.objects.none()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email

        if not self.photo:
            s3_object_name = "default/default-avatar.jpg"
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_S3_REGION_NAME")
            )
            try:
                s3_client.head_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_object_name)
            except ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    local_file_path = os.path.join(base.STATIC_ROOT, 'default-avatar.jpg')
                    try:
                        s3_client.upload_file(local_file_path, AWS_STORAGE_BUCKET_NAME, s3_object_name)
                        print("uploaded default-photo into S3 bucket")
                    except ClientError as e:
                        print(e)
                        print("failed to load file into S3")
                else:
                    print("something went wrong")

            self.photo = s3_object_name

        super(User, self).save(*args, **kwargs)

        group, created = Group.objects.get_or_create(name=self.position)
        print("group", group.name)

        permissions = self.get_role_permissions()
        if set(group.permissions.all()) != set(permissions):
            group.permissions.set(permissions)
            print("permissions", permissions)

        if group not in self.groups.all():
            self.groups.set([group,])
            super(User, self).save(*args, **kwargs)

            print(f"user added to group: {self.groups.all()}")
            self.refresh_from_db()
            print(f"User {self.email} added to group: {self.groups.all()}")

    @property
    def is_staff(self):
        return self.position in {User.Position.TEACHER, User.Position.ADMIN}

    @property
    def is_superuser(self):
        return self.position == User.Position.ADMIN
