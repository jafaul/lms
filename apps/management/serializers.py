from rest_framework import serializers, viewsets

from apps.assessment import serializers as assessment_serializers
from apps.management.models import Course, Task, Lecture


class CourseSerializer(serializers.ModelSerializer):
    students_amount = serializers.SerializerMethodField()

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
