from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text=_('Required. Inform a valid email address.'), required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'photo']

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
        label=_("Select user role")
    )

    class Meta:
        model = User
        fields = ['position']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(help_text=_('Required. Inform a valid email address.'), required=True)
    first_name = forms.CharField(help_text=_('Required. Inform a valid first name.'), required=True)
    last_name = forms.CharField(help_text=_('Required. Inform a valid last name.'), required=True)
    photo = forms.ClearableFileInput(attrs={'multiple': False, "required": False})

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