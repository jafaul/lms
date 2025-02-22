from django.urls import path
# from rest_framework.routers import DefaultRouter

from apps.management import views

# router = DefaultRouter()


urlpatterns = [
    path("", views.CourseListViewSet.as_view(), name="course-list"),
    path("my/", views.MyCourseListViewSet.as_view(), name="my-course-list"),
    path("add/", views.CourseCreateAPIView.as_view(), name="course-create"),
    path("<int:pk>/", views.CourseRetrieveUpdateDestroyAPIView.as_view(), name="course-details"),

    path("<int:pk>/tasks/", views.TaskListViewSet.as_view(), name="task-details"),
    path("<int:pk>/tasks/add", views.TaskCreateAPIView.as_view(), name="task-create"),
    path("<int:pk>/tasks/<int:pktask>", views.TaskRetrieveUpdateDestroyAPIView.as_view(), name="task-details"),

    path("<int:pk>/lectures/", views.LectureListViewSet.as_view(), name="lecture-details"),
    path("<int:pk>/lectures/add", views.LectureCreateAPIView.as_view(), name="lecture-create"),
    path("<int:pk>/lectures/<int:pklecture>", views.LectureRetrieveUpdateDestroyAPIView.as_view(), name="lecture-details")

]
