from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from rest_framework import generics, permissions

from apps.assessment import models, forms, tasks, serializers
from apps.management.models import Task


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
        tasks.send_homework_accepted_email.delay(answer_id=form.instance.id)
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

        tasks.send_mark_notification_email.delay(mark_id=mark.id)

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


class AnswerCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.AnswerSerializer

    def perform_create(self, serializer):
        answer = serializer.save(
            student=self.request.user,
            task=get_object_or_404(Task, pk=self.kwargs["pktask"])
        )
        tasks.send_homework_accepted_email.delay(answer_id=answer.id)


class MarkCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.MarkSerializer

    def perform_create(self, serializer):
        mark = serializer.save(teacher=self.request.user)
        answer = get_object_or_404(models.Answer, pk=self.kwargs["pkanswer"])
        answer.mark = mark
        answer.save()

        tasks.send_mark_notification_email.delay(mark_id=mark.id)


