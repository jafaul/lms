from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from apps.assessment import models, forms
from apps.management.models import Task

from django.utils.translation import gettext_lazy as _


class BaseCreateView(CreateView):
    btn_name = ""
    title = ""
    template_name = "form.html"

    def get_action_url(self):
        raise NotImplemented

    def get_success_url(self):
        return reverse_lazy(
            "management:course-detail", kwargs={"pk": self.kwargs["pk"]}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["action_url"] = self.get_action_url()
        context["btn_name"] = self.btn_name
        context["title"] = self.title
        return context


class AnswerCreateView(PermissionRequiredMixin, LoginRequiredMixin, BaseCreateView):
    model = models.Answer
    form_class = forms.AnswerForm
    btn_name = "Send homework"
    title = "Apply homework"
    template_name = "create_answer.html"

    def get_permission_required(self):
        permissions = [
            f"management.can_access_{self.kwargs['pk']}_course_as_student",
        ]
        return permissions

    def form_valid(self, form):
        form.instance.student = self.request.user
        form.instance.task = get_object_or_404(Task, pk=self.kwargs["pktask"])
        form_valid = super().form_valid(form)

        # send_mail(
        #     "Your homework has been approved",
        #     f"Your homework has been approved: {form.instance.description}",
        #     base.DEFAULT_FROM_EMAIL,
        #     [self.request.user.email]
        # )

        # better for html msg
        print(form.instance.task.title)

        subject = f"Your homework for task '{form.instance.task.title.strip()}' is been received".replace(
            "&#x27;", ""
        )

        full_msg = f"""Please be informed that we have received your homework for the task '{form.instance.task.title}'.
            It will be checked during 7 days."""
        email = EmailMultiAlternatives(
            subject=render_to_string(
                "emails/assessment/subject_answer_send.txt",
                context={"subject": subject},
            ),
            body=render_to_string(
                "emails/assessment/message_answer_send.txt",
                context={"msg": _(full_msg), "request": self.request},
            ).strip(),
            to=[self.request.user.email],
        )
        msg1, msg2 = full_msg.split(".\n", 2)
        relative_url = reverse(
            "management:course-detail", kwargs={"pk": self.kwargs["pk"]}
        )

        course_url = self.request.build_absolute_uri(relative_url)
        print(course_url)
        email.attach_alternative(
            render_to_string(
                "emails/assessment/answer_send.html",
                context={
                    "msg2": _(msg2),
                    "msg1": _(msg1),
                    "request": self.request,
                    "url_btn": course_url,
                },
            ),
            "text/html",
        )
        email.send()

        return form_valid

    def get_action_url(self):
        return reverse_lazy(
            "assessment:create_answer",
            kwargs={"pk": self.kwargs["pk"], "pktask": self.kwargs["pktask"]},
        )


class MarkCreateView(PermissionRequiredMixin, LoginRequiredMixin, BaseCreateView):
    model = models.Mark
    form_class = forms.MarkForm
    btn_name = "Assign mark"
    title = "Assign mark"

    def get_permission_required(self):
        permissions = [
            f"management.can_access_{self.kwargs['pk']}_course_as_teacher",
        ]
        return permissions

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        answer = get_object_or_404(models.Answer, pk=self.kwargs["pkanswer"])
        mark = form.save()
        answer.mark = mark
        answer.save()

        return super().form_valid(form)

    def get_action_url(self):
        return reverse_lazy(
            "assessment:create_mark",
            kwargs={
                "pk": self.kwargs["pk"],
                "pktask": self.kwargs["pktask"],
                "pkanswer": self.kwargs["pkanswer"],
            },
        )
