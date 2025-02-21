from rest_framework import serializers

from apps.assessment.models import Answer, Mark
from apps.authentication.serializers import UserSerializer


class MarkSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Mark
        fields = ["id", "mark_value", "submission_datetime", "teacher"]
        read_only_fields = ["id", "submission_datetime", "teacher"]


class AnswerSerializer(serializers.ModelSerializer):
    mark = MarkSerializer(many=False, read_only=True)
    student = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "description", "student", "mark", "submission_datetime"]
        read_only_fields = ["id", "submission_datetime", "student"]
