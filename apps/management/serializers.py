from rest_framework import serializers

from apps.assessment import serializers as assessment_serializers
from apps.management.models import Course, Task, Lecture
from apps.authentication.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    students_amount = serializers.SerializerMethodField()
    students = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "description", "start_datetime", "tags", "teacher", "students", "students_amount"]

    def get_students_amount(self, obj):
        return obj.students.count()


class TaskSerializer(serializers.ModelSerializer):
    answers = assessment_serializers.AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id", "title", "deadline", "max_mark", "description", "answers"
        ]


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ["id", "title", "description"]


