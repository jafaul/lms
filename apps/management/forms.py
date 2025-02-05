from django import forms
from django.contrib.auth import get_user_model

from apps.management.models import Task, Lecture, Course


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "max_mark", "deadline"]

    def save(self, commit=True):
        task = super(TaskForm, self).save(commit=True)
        task.max_mark = self.cleaned_data["max_mark"]
        task.save()
        return task


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ["title", "description"]


class CourseUpdateForm(forms.ModelForm):
    User = get_user_model()

    class Meta:
        model = Course
        fields = ["students", "teacher"]

    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    teacher = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class CourseCreateForm(forms.ModelForm):
    User = get_user_model()
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name=("student",)),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    teacher = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name=("teacher",)),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Course
        fields = ["teacher", "title", "description", "students"]
