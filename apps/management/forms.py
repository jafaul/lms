from django import forms

from apps.management.models import Task, Lecture


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
