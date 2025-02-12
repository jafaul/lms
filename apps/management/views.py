from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.db.models import Q, Value, Avg, F, FloatField, Sum, IntegerField, Count, Prefetch
from django.db.models.functions import Round, Coalesce
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView
from django_filters.views import FilterView

from apps.assessment.forms import MarkForm
from apps.management import models, forms
from django.utils.translation import gettext_lazy as _

from apps.management.filters import CourseFilterSet, RatingFilter


class CourseListView(FilterView):
    model = models.Course
    template_name = 'course_list.html'
    # paginate_by = 10
    filterset_class = CourseFilterSet

    def get_queryset(self):
        return models.Course.objects.prefetch_related(
            "students"
        ).select_related("teacher").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Courses"

        return context


# @login_required -- func based
class MyCourseListView(LoginRequiredMixin, FilterView):
    model = models.Course
    redirect_field_name = 'next'
    template_name = 'course_list.html'
    filterset_class = CourseFilterSet
    # paginate_by = 5

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
        return models.Course.objects.select_related("teacher").prefetch_related(
            Prefetch("students", queryset=models.User.objects.only("id", "username")),
            "lectures",
            "tasks",
            "tasks__answers",
            "tasks__answers__mark",
            "tasks__answers__student",
            "tasks__answers__mark__teacher"
        ).select_related("teacher")


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

    def form_valid(self, form):

        course = form.save(commit=False)

        if not course.start_datetime:
            return JsonResponse({"error": "Start datetime is missing before saving!"}, status=400)

        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        print(f"DEBUG: Form is invalid. Errors: {form.errors}")
        return super().form_invalid(form)


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


User = get_user_model()


class RatingView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "ratings.html"

    def get_permission_required(self):
        course_id = self.kwargs.get("pk")
        permissions = [
            "management.view_course",
            f"management.can_access_{course_id}_course_as_teacher",
            f"management.can_access_{course_id}_course_as_student",
        ]
        return permissions

    def has_permission(self):
        permissions = self.get_permission_required()
        return any(self.request.user.has_perm(perm) for perm in permissions)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get("pk")
        queryset = User.objects.filter(courses_as_student__id=course_id)

        order_by = self.request.GET.get("order_by", "avg_mark")

        results = (queryset
            .annotate(
                avg_mark=Coalesce(
                    Round(
                        Avg("answers__mark__mark_value", filter=F("answers__task__course_id") == course_id),
                        2
                    ),
                    Value(0.0, output_field=FloatField())
                ),
                total_score=Coalesce(
                    Sum("answers__mark__mark_value", filter=F("answers__task__course_id") == course_id),
                    Value(0, output_field=IntegerField())
                ),
                answers_send=Coalesce(
                    Count("answers", distinct=True, filter=F("answers__task__course_id") == course_id),
                    Value(0, output_field=IntegerField())
                )
            )
            .order_by(F(order_by).desc())
            .prefetch_related("answers__mark")
            .values("id", "first_name", "last_name", "avg_mark", "total_score", "answers_send")
        )

        results = list(results)
        print(results)

        avg_mark_filter = self.request.GET.get("avg_mark", "")
        sum_mark_filter = self.request.GET.get("total_score", "")
        answers_send_filter = self.request.GET.get("answers_send", "")
        print(f"DEBUG: {answers_send_filter=}")

        if any([avg_mark_filter, sum_mark_filter, answers_send_filter]):
            filtered_results = []
            for r in results:
                condition = True
                if avg_mark_filter:
                    condition = condition and r["avg_mark"] >= float(avg_mark_filter)
                if sum_mark_filter:
                    condition = condition and r["total_score"] >= int(sum_mark_filter)
                if answers_send_filter:
                    condition = condition and r["answers_send"] >= int(answers_send_filter)
                    print(f"DEBUG: {condition=}")

                if condition:
                    filtered_results.append(r)

            context["ratings"] = filtered_results
        else:
            context["ratings"] = results
        filterset = RatingFilter(
            self.request.GET, queryset=queryset
        )
        context["filter"] = filterset

        return context


#todo add pagination in users, course detail, courses, add login with social networks

