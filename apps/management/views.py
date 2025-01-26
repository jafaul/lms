from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView


from apps.management import models


# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(f"Hello World, GET: { request.META.get('HTTP_USER_AGENT')}")


# todo https://www.geeksforgeeks.org/software-engineering-coupling-and-cohesion/ ; two scoops of django


# @login_required -- func based
class CourseListView(LoginRequiredMixin, ListView):
    model = models.Course
    redirect_field_name = 'next'  # Where to redirect after login
    template_name = 'course_list.html'


# class CourseCreateView(CreateView):
#     model = models.Course
#     fields = '__all__'
#     success_url = reverse_lazy("management:management_create_course")
#

# class CourseView(TemplateView):
#     def get(self, request, course_id: int):
#         course = models.Course.objects.get(id=course_id)
#         course_data = {
#                 "id": course.id,
#                 "title": course.title,
#                 "description": course.description,
#                 "teacher": course.teacher.username if course.teacher else None,
#                 # "students": [for student in course.students],
#             }
#         return JsonResponse(course_data, safe=False)


