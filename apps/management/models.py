import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.models import User


# Create your models here.


class Course(models.Model):
    teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='courses_as_teacher', null=True)
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)
    students = models.ManyToManyField(
        User, related_name='courses_as_students',
    )

    def __str__(self):
        return f'<Course: {self.title}>'


class Task(models.Model):
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, related_name="tasks"
    )
    title = models.CharField(_("Title"), max_length=100)
    description = models.TextField(_("Description"), max_length=1000)
    max_mark = models.PositiveIntegerField(
        _("Max Mark"), default=5,  validators=[MinValueValidator(1), MaxValueValidator(200)]
    )
    deadline = models.DateField(_("Deadline"), default=datetime.date.today() + datetime.timedelta(days=7), null=True, blank=True)

    def __str__(self):
        return self.title


class Lecture(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="lectures")
    title = models.CharField(_("Title"), max_length=100)
    description = models.TextField(_("Description"), null=True, blank=True)

    def __str__(self):
        return self.title

