from django.urls import path

from apps.home import views

app_name = "apps.home"


urlpatterns = [
    path("", views.HomeView.as_view(), name='home-page')
]
