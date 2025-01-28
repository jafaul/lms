from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
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
    def get_context_data(self, request, course_id: int):
        course = models.Course.objects.get(id=course_id)
        course_data = {
                "title": course.title,
                "description": course.description,
                "teacher": course.teacher.username if course.teacher else None,
                "students": [student for student in course.students],
                "tasks": [task for task in course.tasks],
            }
        return JsonResponse(course_data, safe=False)



# class CourseCreateView(CreateView):
#     model = models.Course
#     fields = '__all__'
#     success_url = reverse_lazy("management:management_create_course")
#
