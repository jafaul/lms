import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

User = get_user_model()


# Create your models here.
class Course(models.Model):
    teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='courses_as_teacher', null=True)
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)
    students = models.ManyToManyField(
        User, related_name='courses_as_student', default=[], blank=True
    )
    start_datetime = models.DateTimeField(_('Start datetime'))
    tags = ArrayField(models.CharField(_('Tags'), max_length=255), default=list)

    def __str__(self):
        return f'<Course: {self.title}>'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        transaction.on_commit(self.assign_permissions)

    def assign_permissions(self):
        content_type = ContentType.objects.get_for_model(Course)

        teacher_perm, created = Permission.objects.get_or_create(
            codename=f"can_access_{self.id}_course_as_teacher",
            name=_(f"Can access {self.title} course as teacher"),
            content_type=content_type,
        )

        students_perm, created = Permission.objects.get_or_create(
            codename=f"can_access_{self.id}_course_as_student",
            name=_(f"Can access {self.title} course as student"),
            content_type=content_type,
        )

        if self.teacher and not self.teacher.has_perm(teacher_perm):
            self.teacher.user_permissions.add(teacher_perm)
            print(f"added permission for teacher: {self.teacher.get_all_permissions()}")

        self.refresh_from_db()

        for student in self.students.all():
            if not student.has_perm(students_perm):
                student.user_permissions.add(students_perm)
                print(f"added permission for student {student.email}: {student.get_all_permissions()}")


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

