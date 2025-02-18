from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm as BasePasswordResetForm, \
    SetPasswordForm as BaseSetPasswordForm, SetPasswordMixin as BaseSetPasswordMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm

from apps.authentication import tasks
from apps.authentication.tokens import account_activation_token

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg", "id": "inputFirstName",
                "required": True,
            })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg", "id": "inputLastName",
                "required": True,
            })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg", "id": "inputEmail",
                "required": "",
            })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg", "id": "inputPassword",
                "required": "",
            })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg", "id": "inputPassword1",
                "required": "",
            })
    )


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        exclude = ["photo"]

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        print("start to save user")
        if commit:
            print("User saved!")
            user.save()
        return user


class PasswordResetForm(BasePasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg", "id": "inputEmail",
                "required": "",
            })
    )

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email,
                  html_email_template_name=None):
        pass


class SetPasswordMixin(BaseSetPasswordMixin):
    @staticmethod
    def create_password_fields(label1=_("Password"), label2=_("Password confirmation")):
        password1 = forms.CharField(
            label=label1,
            required=True,
            strip=False,
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control form-control-lg"}),
            help_text=password_validation.password_validators_help_text_html(),
        )
        password2 = forms.CharField(
            label=label2,
            required=True,
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control form-control-lg"}),
            strip=False,
            help_text=_("Enter the same password as before, for verification."),
        )
        return password1, password2


class SetPasswordForm(BaseSetPasswordForm):
    new_password1, new_password2 = SetPasswordMixin.create_password_fields(
        label1=_("New password"), label2=_("New password confirmation")
    )


class UserAssignmentRoleForm(forms.ModelForm):
    position = forms.ChoiceField(
        choices=get_user_model().Position.choices,
        required=True,
        label=_("Select user role"),
    )

    class Meta:
        model = User
        fields = ['position']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        help_text=_('Required. Inform a valid email address.'),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control", "id": "inputEmail", "placeholder": "Email address",
                "required": "", "autofocus": "",
            })

    )

    first_name = forms.CharField(
        help_text=_('Required. Inform a valid first name.'), required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control", "id": "inputFirstName", "placeholder": "First Name",
                "required": True,
            })
    )
    last_name = forms.CharField(
        help_text=_('Required. Inform a valid last name.'), required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control", "id": "inputLastName", "placeholder": "Last Name",
                "required": True,
            })
    )

    photo = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control-file",
                "id": "inputFile",
                "placeholder": "Upload Photo",
            }
        ),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'photo']

        help_texts = {
            "photo": "Upload a profile picture (optional).",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg", "id": "typeEmailX",
                "required": "", "autofocus": "", "type": "email"
            })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg", "id": "inputPassword",
                "required": "",
            })
    )