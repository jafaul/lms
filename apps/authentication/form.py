from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='Required. Inform a valid email address.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

