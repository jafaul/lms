from rest_framework import serializers

from apps.assessment.models import Answer, Mark


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ["id", "mark_value", "submission_datetime"]
        read_only_fields = ["id", "submission_datetime"]


class AnswerSerializer(serializers.ModelSerializer):
    mark = MarkSerializer(many=False, read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "description", "student", "mark", "submission_datetime"]
        read_only_fields = ["id", "submission_datetime"]
