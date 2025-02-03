from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    help = "Set up permissions for groups"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # set all permissions for superuser
        admin_group, _ = Group.objects.get_or_create(name='admin')
        all_permissions = Permission.objects.all()
        admin_group.permissions.set(all_permissions)

        # set permissions for manager
        manager_group, _ = Group.objects.get_or_create(name='manager')
        manager_permissions = Permission.objects.filter(
            codename__endswith="_lecture"
        )
        manager_group.permissions.set(manager_permissions)

        # set permissions for teacher
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        teacher_permissions = Permission.objects.filter(
            Q(codename__endswith="_task") |
            Q(codename__endsswith="_mark") |
            Q(codename="view_answer") |
            Q(codename="view_course")
        )
        teacher_group.permissions.set(teacher_permissions)

        # set permissions for student
        student_group, _ = Group.objects.get_or_create(name='student')
        student_permissions = Permission.objects.filter(
            Q(codename__endswith="view_mark") |
            Q(codename__endsswith="_answer") |
            Q(codename="view_task") |
            Q(codename="view_lecture") |
            Q(codename="view_user") |
            Q(codename="view_course")
        )
        student_group.permissions.set(student_permissions)


