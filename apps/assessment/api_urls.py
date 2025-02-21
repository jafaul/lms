from django.urls import path

from apps.assessment import views

urlpatterns = [
    # create views
    path("answers/add/", views.AnswerCreateAPIView.as_view(), name='create-answer'),
    path("answers/<int:pkanswer>/mark/add/", views.MarkCreateAPIView.as_view(), name='create_mark'),
]