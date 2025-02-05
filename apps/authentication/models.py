from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _



class SchoolUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
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

    def get_role_permissions(self):
        if self.position == self.Position.ADMIN:
            return Permission.objects.all()
        elif self.position == self.Position.MANAGER:
            return Permission.objects.filter(Q(codename__endswith="_lecture")|Q(codename="view_course"))
        elif self.position == self.Position.TEACHER:
            return Permission.objects.none()
        elif self.position == self.Position.STUDENT:
            return Permission.objects.none()

        return Permission.objects.none()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email

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
