from django import forms

from apps.assessment import models


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ["description"]

    def save(self, commit=True):
        answer = super(AnswerForm, self).save(commit=True)
        answer.save()
        return answer


class MarkForm(forms.ModelForm):
    class Meta:
        model = models.Mark
        fields = ["mark_value"]

    def save(self, commit=True):
        mark = super(MarkForm, self).save(commit=True)
        mark.save()
        return mark
