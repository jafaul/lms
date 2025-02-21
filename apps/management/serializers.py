from rest_framework import serializers, viewsets

from apps.management.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "description", "start_datetime", "tags", "teacher", "students"]


class CourseListViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.prefetch_related("students").select_related("teacher").order_by("start_datetime").all()
    serializer_class = CourseSerializer
