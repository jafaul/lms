from django.urls import path

from apps.about.views import AboutView

urlpatterns = [
    path('whoami/', AboutView.as_view(), name='whoami'),
]
