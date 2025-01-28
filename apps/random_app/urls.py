from django.urls import path

from apps.random_app.views import RandomView

urlpatterns = [
    path("", RandomView.as_view(), name='random_view')
]
