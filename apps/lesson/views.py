from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.

class HomeView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, world. You're at the polls home view.")


def home_functional_view(request):
    return HttpResponse("Functional Hello")