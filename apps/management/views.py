from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation.template import context_re

from django.views.generic import ListView, CreateView, TemplateView

from apps.management import models


class CourseListView(ListView):
    model = models.Course
    template_name = 'course_list.html'

    def get_queryset(self):
        return models.Course.objects.prefetch_related(
            "students"
        ).select_related("teacher").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Courses"

        return context


# @login_required -- func based
class MyCourseListView(LoginRequiredMixin, ListView):
    model = models.Course
    redirect_field_name = 'next'
    template_name = 'course_list.html'

    def get_queryset(self):
        return models.Course.objects.prefetch_related(
            "students"
        ).select_related("teacher").filter(students=self.request.user).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My Courses"

        return context


class CourseView(TemplateView):
    template_name = 'course_detail.html'

    def get_context_data(self, course_id: int, **kwargs):
        get_object_or_404(models.Course, id=course_id)

        course = models.Course.objects.prefetch_related(
            "students",
            "lectures",
            "tasks",
            "tasks__responses",
            "tasks__responses__mark__mark_value"
        ).select_related(
            "teacher"
        ).get(id=course_id)

        context = super().get_context_data(**kwargs)
        context['course'] = course
        context['lectures'] = course.lectures.all()
        context['tasks'] = course.tasks.all()

        return context



# class CourseCreateView(CreateView):
#     model = models.Course
#     fields = '__all__'
#     success_url = reverse_lazy("management:management_create_course")
#
