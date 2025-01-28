from django.urls import path

from apps.management import views

app_name = "apps.management"


urlpatterns = [
    path("", views.CourseListView.as_view(), name='all_courses'),
    path("my/", views.MyCourseListView.as_view(), name='my_courses'),

    # path("courses/<int:course_id>/", CourseView.as_view(), name='management_course_by_id'),
    # path("courses/add/", CourseCreateView.as_view(), name='management_create_course'),

]
