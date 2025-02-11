from django.urls import path

from .views import HomeView, home_functional_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("hello-functional/", home_functional_view, name="home-functional")
]
