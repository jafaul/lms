from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


# # Create your views here.
# class HomeView(TemplateView):
#     template_name = 'home.html'

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
