from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.authentication.views import LoginView, UserSettingsView, UserRegistrationView, UserProfileView, \
    UsersProfilesView, PositionAddView

app_name = "apps.authentication"


urlpatterns = [
    path("login/", LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('settings/', UserSettingsView.as_view(), name='settings'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/', UsersProfilesView.as_view(), name='users-profiles'),
    path('users/<int:pk>/position/', PositionAddView.as_view(), name='update-role'),

]
