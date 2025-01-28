from django.urls import path

from apps.management import views

app_name = "apps.management"


urlpatterns = [
    path("", views.CourseListView.as_view(), name='all-courses'),
    path("my/", views.MyCourseListView.as_view(), name='my-courses'),

    path("<int:course_id>/", views.CourseView.as_view(), name='course-detail'),
    # path("courses/add/", CourseCreateView.as_view(), name='management_create_course'),

]
