from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm


User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", "id": "inputFirstName", "placeholder": "First Name",
                "required": True,
            })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", "id": "inputLastName", "placeholder": "Last Name",
                "required": True,
            })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control", "id": "inputEmail", "placeholder": "Email address",
                "required": "", "autofocus": "",
            })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", "id": "inputPassword", "placeholder": "Password",
                "required": "",
            })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", "id": "inputPassword1", "placeholder": "Repeat Password",
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
                "class": "form-control", "id": "inputEmail", "placeholder": "Email address",
                "required": "", "autofocus": "",
            })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", "id": "inputPassword", "placeholder": "Password",
                "required": "",
            })
    )