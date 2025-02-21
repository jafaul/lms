from rest_framework.routers import DefaultRouter

from apps.management.serializers import CourseListViewSet

router = DefaultRouter()
router.register(r'courses', CourseListViewSet, basename='courses')
