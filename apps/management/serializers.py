from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.assessment import serializers as assessment_serializers
from apps.management.models import Course, Task, Lecture
from apps.authentication.serializers import UserSerializer

User = get_user_model()


class CourseSerializer(serializers.ModelSerializer):
    """
    {
        "title": "course name",
        "description": "course desc",
        "start_datetime": "2025-03-01T10:00:00Z",
        "tags": ["test"],
        "teacher_id": 97,
        "students_ids": [94, 95]
    }
    """

    students_amount = serializers.SerializerMethodField()
    students = UserSerializer(many=True, read_only=True)
    teacher = UserSerializer(read_only=True)

    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(position__in=["teacher", "admin", "manager"]).all(), write_only=True
    )
    students_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, many=True
    )

    class Meta:
        model = Course
        fields = [
            "id", "title", "description", "start_datetime", "tags", "teacher", "students", "students_amount",
            "teacher_id", "students_ids"
        ]
        read_only_fields = ["id", "students_amount", "students", "teacher"]

    def get_students_amount(self, obj):
        return obj.students.count()

    def create(self, validated_data):
        students = validated_data.pop("students_ids", [])
        teacher = validated_data.pop("teacher_id", None)

        course = Course.objects.create(**validated_data)
        course.teacher = teacher
        course.students.set(students)
        return course


class TaskSerializer(serializers.ModelSerializer):
    """
    {
        "title": "new task",
        "deadline": "2025-03-01",
        "max_mark": 5,
        "description": "desc"
    }
    """

    answers = assessment_serializers.AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id", "title", "deadline", "max_mark", "description", "answers"
        ]
        read_only_fields = ["id", "answers"]


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ["id", "title", "description"]
        read_only_fields = ["id"]


