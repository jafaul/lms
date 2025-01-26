from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.utils.translation import gettext_lazy as _

User = get_user_model()


# Create your models here.
class Response(models.Model):
    task = models.ForeignKey("management.Task", on_delete=models.CASCADE)
    description = models.TextField(_("Description"), max_length=500)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_datetime = models.DateTimeField(
        _("Submission datetime"), auto_now_add=True, blank=True, null=False)

    def __str__(self):
        return self.description


class Mark(models.Model):
    answer = models.OneToOneField(Response, on_delete=models.CASCADE)
    submission_datetime = models.DateTimeField(_("Submission datetime"), blank=True, null=False, auto_now=True)
    mark_value = models.IntegerField(
        _("Mark value"), default=5, validators=[MinValueValidator(1), MaxValueValidator(200)])
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.mark_value
