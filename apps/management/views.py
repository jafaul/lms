from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, DetailView, UpdateView

from apps.management import models, forms
from apps.management.models import Course
from django.utils.translation import gettext_lazy as _


class CourseListView(PermissionRequiredMixin, ListView):
    model = models.Course
    template_name = 'course_list.html'
    permission_required = ("apps.management.view_course",)

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


class CourseDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    template_name = 'course_detail.html'
    model = models.Course
    context_object_name = 'course'  # to use "course" obj in template

    def get_permission_required(self):
        course = self.get_object()
        permissions = [
            "apps.management.view_course",
            f"can_access_{course.id}_course_as_teacher",
            f"can_access_{course.id}_course_as_student",
        ]
        return permissions

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
    fields = '__all__'
    template_name = 'form.html'
    permission_required = ["apps.management.create_course", ]

    def get_success_url(self):
        return reverse_lazy('management:course-detail', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Course"
        context["action_url"] = reverse_lazy("management:create_course")
        context["btn_name"] = "Create"
        return context

    def form_valid(self, form):
        course = form.save(commit=False)
        course.save()

        teacher_permission = Permission(
            content_type=ContentType.objects.get_for_model(Course),
            codename=f"can_access_{course.id}_course_as_teacher",
            name=_(f"Can access {course.id} course as teacher")
        )
        teacher_permission.save()
        course.teacher.user_permissions.add(teacher_permission)

        student_permission = Permission(
            content_type=ContentType.objects.get_for_model(Course),
            codename=f"can_access_{course.id}_course_as_student",
            name=_(f"Can access {course.id} course as student")
        )
        student_permission.save()

        for student in course.students.all():
            student.user_permissions.add(student_permission)

        return super().form_valid(form)


class UpdateCourseView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = models.Course
    form_class = forms.CourseUpdateForm
    template_name = 'form.html'
    permission_required = ('apps.management.change_course',)

    def get_success_url(self):
        return reverse_lazy('management:course-detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update"
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

    title = "Add Task"
    action_url_name = "management:create-task"
    btn_name = "Add task"

    def get_permission_required(self):
        permissions = [
            f"can_access_{self.kwargs['pk']}_course_as_teacher",
        ]
        return permissions


class LectureCreateView(PermissionRequiredMixin, LoginRequiredMixin, BaseCreateView):
    model = models.Lecture
    form_class = forms.LectureForm

    title = "Create Lecture"
    action_url_name = "management:create-lecture"
    btn_name = "Create lecture"

    permission_required = ("apps.management.create_lecture", )

