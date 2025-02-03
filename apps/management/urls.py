from django.urls import path

from apps.management import views

app_name = "apps.management"


urlpatterns = [
    # list views
    path("", views.CourseListView.as_view(), name='all-courses'),
    path("my/", views.MyCourseListView.as_view(), name='my-courses'),
    # detail views
    path("<int:pk>/", views.CourseDetailView.as_view(), name='course-detail'),
    # create views
    path("add/", views.CourseCreateView.as_view(), name='create_course'),
    path("<int:pk>/tasks/add/", views.TaskCreateView.as_view(), name='create-task'),
    path("<int:pk>/lectures/add/", views.LectureCreateView.as_view(), name='create-lecture'),
    # update views
    path("<int:pk>/students/update", views.UpdateCourseView.as_view(), name='update-course'),

]
