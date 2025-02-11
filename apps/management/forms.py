from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, get_current_timezone, is_naive, now
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

    start_datetime = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={
            "type": "datetime-local",
            "class": "form-control",
            "id": "start-datetime",
        })
    )

    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
               'placeholder': _('Enter tags separated by commas'),
               'class': 'form-control',
               'id': 'tags',
               }
        ),
        help_text=_("Enter tags separated by commas (e.g. python, django, programming)")
    )


    class Meta:
        model = Course
        fields = ["teacher", "title", "description", "students", "tags", "start_datetime"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        teachers = self.User.objects.filter(groups__name="teacher")
        self.fields['teacher'].queryset = teachers
        self.fields['teacher'].choices = [("", _(""))] + list(self.fields['teacher'].choices)[1:]

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if not tags:
            return []
        return [tag.strip() for tag in tags.split(',') if tag.strip()]

    def clean_start_datetime(self):
        start_datetime = self.cleaned_data.get('start_datetime')

        if not start_datetime:
            raise ValidationError("Start datetime is required.")

        if is_naive(start_datetime):
            start_datetime = make_aware(start_datetime)

        if start_datetime <= now():
            raise ValidationError("Start date cannot be today or in the past.")
        return start_datetime
