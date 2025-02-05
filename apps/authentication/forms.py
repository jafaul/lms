from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text=_('Required. Inform a valid email address.'), required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

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
        model = get_user_model()
        fields = ['position']

    def save(self, commit=True):
        user = super(UserAssignmentRoleForm, self).save(commit=False)
        user.grous.clear()
        position = self.cleaned_data['position']
        group, created = Group.objects.get_or_create(name=position)

        user.groups.add(group)
        if commit:
            user.save()
        return user

