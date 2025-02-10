from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

User = get_user_model()


# Create your models here.
class Answer(models.Model):
    task = models.ForeignKey("management.Task", on_delete=models.CASCADE, related_name="answers")
    description = HTMLField(_("Description"), max_length=500)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    submission_datetime = models.DateTimeField(
        _("Submission datetime"), auto_now_add=True, blank=True, null=False)
    mark = models.OneToOneField(
        "assessment.Mark", on_delete=models.CASCADE, null=True, blank=True, related_name="answer"
    )  # one to one rel

    def __str__(self):
        return self.description


class Mark(models.Model):
    submission_datetime = models.DateTimeField(_("Submission datetime"), blank=True, null=False, auto_now=True)
    mark_value = models.IntegerField(
        _("Mark value"), default=5, validators=[MinValueValidator(1), MaxValueValidator(200)])
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.mark_value)
