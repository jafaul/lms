from django.db.migrations import CreateModel
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

from django.views.generic import TemplateView

from apps.management import models


# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(f"Hello World, GET: { request.META.get('HTTP_USER_AGENT')}")


# todo read about csrf

class CourseListView(ListView):
    model = models.Course

    # template_name = 'course/course_list.html'

    # pass variables to django tmp view
    # def get_context_data(self, **kwargs):
    #     return {"courses": models.Course.objects.all()}

    # def get(self, request, *args, **kwargs):
    #     courses = models.Course.objects.all()
    #     courses_list = [
    #         {
    #             "id": course.id,
    #             "title": course.title,
    #             "description": course.description,
    #             "teacher": course.teacher.username if course.teacher else None,
    #         }
    #         for course in courses
    #     ]
    #
    #     return JsonResponse(courses_list, safe=False)

class CourseCreateView(CreateView):
    model = models.Course
    fields = '__all__'
    success_url = reverse_lazy("management:management_create_course")

class CourseView(TemplateView):
    def get(self, request, course_id: int):
        course = models.Course.objects.get(id=course_id)
        course_data = {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "teacher": course.teacher.username if course.teacher else None,
                # "students": [for student in course.students],
            }
        return JsonResponse(course_data, safe=False)


