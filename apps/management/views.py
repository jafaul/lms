from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, DetailView

from apps.management import models, forms


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


class CourseDetailView(DetailView):
    template_name = 'course_detail.html'
    model = models.Course
    context_object_name = 'course'  # to use "course" obj in template

    def get_queryset(self):
        course = models.Course.objects.prefetch_related(
            "students",
            "lectures",
            "tasks",
            "tasks__answers",
            "tasks__answers__mark__mark_value"
        ).select_related("teacher")

        return course


class CourseCreateView(CreateView):
    model = models.Course
    fields = '__all__'
    template_name = 'form.html'

    def get_success_url(self):
        return reverse_lazy('management:course-detail', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Course"
        context["action_url"] = reverse_lazy("management:create_course")
        context["btn_name"] = "Create"
        return context


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


class TaskCreateView(BaseCreateView):
    model = models.Task
    form_class = forms.TaskForm

    title = "Add Task"
    action_url_name = "management:create-task"
    btn_name = "Add task"


class LectureCreateView(BaseCreateView):
    model = models.Lecture
    form_class = forms.LectureForm

    title = "Create Lecture"
    action_url_name = "management:create-lecture"
    btn_name = "Create lecture"
