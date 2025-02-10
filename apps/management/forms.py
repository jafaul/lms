from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.management.models import Task, Lecture, Course


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        label=_("Title"),
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control", "id": "title",
        }),
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "id": "desc",
        })
    )

    max_mark = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "id": "max_mark",
        })
    )
    deadline = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            "class": "form-control",
            "type": "date",
            "id": "deadline",
        })
    )


    class Meta:
        model = Task
        fields = ["title", "description", "max_mark", "deadline"]

    def save(self, commit=True):
        task = super(TaskForm, self).save(commit=False)
        task.max_mark = self.cleaned_data["max_mark"]
        task.save()
        return task


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ["title", "description"]

    title = forms.CharField(
        label=_("Title"),
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control", "id": "title",
        }),
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "id": "desc",
        })
    )

class CourseUpdateForm(forms.ModelForm):
    User = get_user_model()

    class Meta:
        model = Course
        fields = ["students", "teacher"]

    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )

    teacher = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )


User = get_user_model()

class CourseCreateForm(forms.ModelForm):
    User = get_user_model()
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name="student"),
        required=False,
        # empty_label=None,
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-select",
                "id": "students",
            }
        ),
    )

    teacher = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "teacher",
        }),
    )

    title = forms.CharField(
        label=_("Title"),
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control", "id": "title",
        }),
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "id": "desc",
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        teachers = self.User.objects.filter(groups__name="teacher")
        self.fields['teacher'].queryset = teachers
        self.fields['teacher'].choices = [("", _(""))] + list(self.fields['teacher'].choices)[1:]

    class Meta:
        model = Course
        fields = ["teacher", "title", "description", "students"]
