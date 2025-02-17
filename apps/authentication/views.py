from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.encoding import  force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView, UpdateView, ListView

from apps.authentication.tokens import account_activation_token
from apps.authentication.tasks import activate_email
from apps.authentication import forms

User = get_user_model()


class LoginView(BaseLoginView):
    redirect_authenticated_user = True
    template_name = "login.html"
    form_class = forms.LoginForm

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Invalid username or password.')
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
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            activate_email.delay(user_id=user.id)

            messages.add_message(
                self.request, messages.SUCCESS,
                f'Dear <b>{user}</b>, please go to you email <b>{user.email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.'
            )
            return redirect('apps.authentication:profile')
        else:
            for error in list(form.errors.values()):
                messages.add_message(self.request, messages.ERROR, error)
            return render(
                request=request,
                template_name='register.html',
                context={'form': form}
            )


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(self.request, messages.SUCCESS, "Thank you for confirming your email.")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home:home-page')

        messages.add_message(self.request, messages.ERROR, "Activation link is invalid!")
        return redirect('home:home-page')


class PositionAddView(PermissionRequiredMixin, UpdateView):
    template_name = "form.html"
    form_class = forms.UserAssignmentRoleForm
    permission_required = "authentication.change_position"
    model = User
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
    model = User
    context_object_name = "users"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.UserAssignmentRoleForm()
        return context