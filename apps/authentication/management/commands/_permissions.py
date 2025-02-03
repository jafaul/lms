from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from apps.management.models import Course
from django.utils.translation import gettext_lazy as _


class TeacherPermission(Permission):

    def __init__(self, course):
        self.content_type = ContentType.objects.get_for_model(Course)
        self.codename = f"can_access_{course.id}_course_as_teacher"
        self.name = _(f"Can access {course.id} course as teacher")
        super().__init__(content_type=self.content_type, codename=self.codename, name=self.name)

    def has_permission(self, user, course):
        return user.id == course.teacher.id


class StudentPermission(Permission):

    def __init__(self, course):
        self.content_type = ContentType.objects.get_for_model(Course)
        self.codename = f"can_access_{course.id}_course_as_student"
        self.name = f"Can access {course.id} course as student"
        super().__init__(content_type=self.content_type, codename=self.codename, name=self.name)

    def has_permission(self, user, course):
        return user in course.students.all()

