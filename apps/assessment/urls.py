from django.urls import path

from apps.assessment import views

app_name = "apps.management"


urlpatterns = [
    # create views
    path("answers/add/", views.AnswerCreateView.as_view(), name='create_answer'),
    path("answers/<int:pkanswer>/mark/add/", views.MarkCreateView.as_view(), name='create_mark'),
]
