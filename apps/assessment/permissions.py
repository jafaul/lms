from apps.management.permissions import BasePermission


class MarkAccessPermission(BasePermission):
    def get_change_permissions(self, obj):
        return [
            "assessment.add_mark",
            "assessment.change_mark",
            "assessment.delete_mark",
            f"management.can_access_{obj.id}_course_as_teacher",
        ]

    def get_view_permissions(self, obj):
        return [
            "assessment.view_mark",
            f"management.can_access_{obj.id}_course_as_teacher",
            f"management.can_access_{obj.id}_course_as_student",
        ]


class AnswerAccessPermission(BasePermission):
    def get_change_permissions(self, obj):
        return [
            f"management.can_access_{obj.id}_course_as_student",
            "assessment.add_answer",
            "assessment.change_answer",
            "assessment.delete_answer",
        ]

    def get_view_permissions(self, obj):
        return [
            f"management.can_access_{obj.id}_course_as_student",
            f"management.can_access_{obj.id}_course_as_teacher",
            "assessment.view_answer",
        ]