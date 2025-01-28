from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


# Create your views here.

class AboutView(View):
    def get(self, request, *args, **kwargs):
        data = {
            "user_agent": request.META.get("HTTP_USER_AGENT"),
            "IP": request.META.get('REMOTE_ADDR'),
            "timestamp": datetime.now().isoformat(),
        }
        return JsonResponse(data)
