from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, UpdateView, ListView

from apps.authentication import forms

User = get_user_model()


class LoginView(BaseLoginView):
    redirect_authenticated_user = True
    template_name = "login.html"

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return self.render_to_response(self.get_context_data(form=form))


class UserSettingsView(LoginRequiredMixin, UpdateView):
    template_name = 'settings.html'
    form_class = forms.UserUpdateForm
    model = User
    success_url = reverse_lazy("authentication:settings")

    def get_object(self, queryset=None):
        return self.request.user


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


class UserRegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('apps.authentication:profile')
        form = forms.UserRegistrationForm(request.GET or None)
        return render(
            request=request,
            template_name='register.html',
            context={'form': form}
        )

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('apps.authentication:profile')
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            login(request, user)
            return redirect('apps.authentication:profile')
        else:
            for error in list(form.errors.values()):
                print(request, error)
            return render(
                request=request,
                template_name='register.html',
                context={'form': form}
            )


class PositionAddView(PermissionRequiredMixin, UpdateView):
    template_name = "form.html"
    form_class = forms.UserAssignmentRoleForm
    permission_required = "authentication.change_position"
    model = get_user_model()
    queryset = model.objects.all()

    def get_success_url(self):
        return reverse_lazy('apps.authentication:users-profiles')

    def form_valid(self, form):
        user = form.save(commit=False)
        position = form.cleaned_data['position']
        if position:
            user.position = position
            user.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["action_url"] = reverse_lazy(
            "apps.authentication:update-role",
            kwargs={"pk": self.kwargs["pk"]}
        )
        context["btn_name"] = "Assign position"
        context["title"] = "Assign position"
        return context


class UsersProfilesView(PermissionRequiredMixin, ListView):
    permission_required = "authentication.view_user"
    template_name = "users.html"
    model = get_user_model()
    context_object_name = "users"
