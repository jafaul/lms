from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from apps.authentication.form import UserRegistrationForm


# Create your views here.

class LoginView(BaseLoginView):
    redirect_authenticated_user = True
    template_name = "login.html"

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return self.render_to_response(self.get_context_data(form=form))


class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'


class UserRegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('apps.management:my_courses')
        form = UserRegistrationForm(request.GET or None)
        return render(
            request=request,
            template_name='register.html',
            context={'form': form}
        )

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('apps.management:my_courses')
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            login(request, user)
            return redirect('apps.management:my_courses')
        else:
            for error in list(form.errors.values()):
                print(request, error)
            return render(
                request=request,
                template_name='register.html',
                context={'form': form}
            )

