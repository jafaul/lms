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

    def save(self, commit=True):
        lecture = super(LectureForm, self).save(commit=True)
        lecture.save()
        return lecture


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