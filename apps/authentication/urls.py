from django.contrib.auth import views as auth_views
from django.urls import path

from apps.authentication import views

app_name = "apps.authentication"


urlpatterns = [
    path("login/", views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),

    path('settings/', views.UserSettingsView.as_view(), name='settings'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),

    path('users/', views.UsersProfilesView.as_view(), name='users-profiles'),
    path('users/<int:pk>/position/', views.PositionAddView.as_view(), name='update-role'),

    path('activate/<uidb64>/<token>', views.ActivateView.as_view(), name='activate'),

    path("reset_password/", views.PasswordResetView.as_view(), name='reset-password'),

    path(r"reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
