from rest_framework import permissions
from rest_framework.permissions import BasePermission as CoreBasePermissions


class BasePermission(CoreBasePermissions):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def get_view_permissions(self, obj):
        raise NotImplemented

    def get_change_permissions(self, obj):
        raise NotImplemented

    def has_object_permission(self, request, view, obj):
        view_permissions = self.get_view_permissions(obj)
        edit_permissions = self.get_change_permissions(obj)

        if request.method in permissions.SAFE_METHODS:
            # allow student to retrieve course
            return any(request.user.has_perm(perm) for perm in view_permissions)

        return any(request.user.has_perm(perm) for perm in edit_permissions)


class CourseAccessPermission(BasePermission):
    def get_view_permissions(self, obj):
        view_permissions = [
            "management.view_course",
            f"management.can_access_{obj.id}_course_as_teacher",
            f"management.can_access_{obj.id}_course_as_student",
        ]
        return view_permissions

    def get_change_permissions(self, obj):
        change_permissions = [
            "management.add_course",
            "management.change_course",
            "management.delete_course",
            "management.update_course",
        ]
        return change_permissions


class TaskAccessPermission(BasePermission):
    def get_view_permissions(self, obj):
        view_permissions = [
            "management.view_task",
            f"management.can_access_{obj.id}_course_as_teacher",
            f"management.can_access_{obj.id}_course_as_student",
        ]
        return view_permissions

    def get_change_permissions(self, obj):
        change_permissions = [
            "management.change_task",
            "management.delete_task",
            "management.update_task",
            "management.add_task",
            f"management.can_access_{obj.id}_course_as_teacher",
        ]
        return change_permissions


class LectureAccessPermission(BasePermission):
    def get_view_permissions(self, obj):
        return [
            "management.view_lecture",
            f"management.can_access_{obj.id}_course_as_teacher",
            f"management.can_access_{obj.id}_course_as_student",
        ]

    def get_change_permissions(self, obj):
        return [
            "management.change_lecture",
            "management.delete_lecture",
            "management.update_lecture",
            "management.add_lecture",
        ]
