from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, FormView

from apps.authentication import forms


# Create your views here.

class LoginView(BaseLoginView):
    redirect_authenticated_user = True
    template_name = "login.html"

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return self.render_to_response(self.get_context_data(form=form))


class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


class UserRegistrationView(FormView):
    template_name = "register.html"
    form_class = forms.UserRegistrationForm

