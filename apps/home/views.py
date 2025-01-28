from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(f"Hello World, GET: { request.META.get('HTTP_USER_AGENT')}")
