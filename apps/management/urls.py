from django.urls import path

from apps.management.views import HomeView, CourseListView

app_name = "apps.management"


urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("courses/", CourseListView.as_view(), name='management_courses'),
    # path("courses/<int:course_id>/", CourseView.as_view(), name='management_course_by_id'),
    # path("courses/add/", CourseCreateView.as_view(), name='management_create_course'),

]
