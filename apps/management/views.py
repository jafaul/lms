from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, DetailView, UpdateView

from apps.assessment.forms import MarkForm
from apps.management import models, forms
from django.utils.translation import gettext_lazy as _


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
        ).select_related(
            "teacher"
        ).filter(Q(students=self.request.user) | Q(teacher=self.request.user)).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My Courses"

        return context


class CourseDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    template_name = 'course_detail.html'
    model = models.Course
    context_object_name = 'course'  # to use "course" obj in template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mark_form"] = MarkForm
        return context

    def get_permission_required(self):
        course = self.get_object()
        permissions = [
            "management.view_course",
            f"management.can_access_{course.id}_course_as_teacher",
            f"management.can_access_{course.id}_course_as_student",
        ]
        return permissions

    def has_permission(self):
        permissions = self.get_permission_required()
        return any(self.request.user.has_perm(perm) for perm in permissions)

    def get_queryset(self):
        course = models.Course.objects.prefetch_related(
            "students",
            "lectures",
            "tasks",
            "tasks__answers",
            "tasks__answers__mark",
            "tasks__answers__student",
            "tasks__answers__mark__teacher"
        ).select_related("teacher")

        return course


class CourseCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = models.Course
    template_name = 'create_course.html'
    permission_required = ["apps.management.add_course", ]
    form_class = forms.CourseCreateForm

    def get_success_url(self):
        return reverse_lazy('management:course-detail', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Course"
        context["action_url"] = reverse_lazy("management:create_course")
        context["btn_name"] = "Create"
        return context


class UpdateCourseView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = models.Course
    form_class = forms.CourseUpdateForm
    template_name = 'update_course.html'
    permission_required = ('apps.management.change_course',)

    def get_success_url(self):
        return reverse_lazy('management:course-detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = self.object
        context["title"] = "Update course"
        context["action_url"] = reverse_lazy("management:update-course", kwargs={"pk": self.kwargs['pk']})
        context["btn_name"] = "Register"
        return context

    def form_valid(self, form):
        course = form.save(commit=False)
        new_students = form.cleaned_data['students']
        if new_students:
            course.students.add(*new_students)
        course.save()
        return HttpResponseRedirect(self.get_success_url())


class BaseCreateView(CreateView):
    action_url_name = ""
    btn_name = ""
    title = ""
    template_name = 'form.html'

    def get_success_url(self):
        return reverse_lazy('management:course-detail', kwargs={"pk": self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.course = get_object_or_404(models.Course, id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_url"] = reverse_lazy(self.action_url_name, kwargs={"pk": self.kwargs['pk']})
        context["btn_name"] = self.btn_name

        context["title"] = self.title
        return context


class TaskCreateView(PermissionRequiredMixin, LoginRequiredMixin, BaseCreateView):
    model = models.Task
    form_class = forms.TaskForm

    title = _("Add Task")
    action_url_name = "management:create-task"
    btn_name = _("Add task")

    template_name = "create_task.html"

    def get_permission_required(self):
        permissions = [
            f"management.can_access_{self.kwargs['pk']}_course_as_teacher",
        ]
        return permissions


class LectureCreateView(PermissionRequiredMixin, LoginRequiredMixin, BaseCreateView):
    model = models.Lecture
    form_class = forms.LectureForm

    title = _("Create Lecture")
    action_url_name = "management:create-lecture"
    btn_name = _("Create lecture")

    template_name = "create_lecture.html"

    permission_required = ("management.add_lecture", )

    def has_permission(self):
        return super().has_permission()

