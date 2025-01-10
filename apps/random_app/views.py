import random
import string

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.

#  /random?length=42&specials=1&digits=0
class RandomView(View):
    def get(self, request, *args, **kwargs):
        try:
            length = int(request.GET.get("length", 8))
            specials = int(request.GET.get("specials", 0))
            digits = int(request.GET.get("digits", 0))
        except ValueError:
            return HttpResponse("Digits must be and integer", status=400)

        if length > 100 or length < 1:
            return HttpResponse("Length must be between 1 and 100", status=400)
        if specials not in {0, 1}:
            return HttpResponse("Specials must be 0 or 1", status=400)
        if digits not in {0, 1}:
            return HttpResponse("Digits must be 0 or 1", status=400)

        all_characters = string.ascii_letters
        if specials:
            all_characters += string.punctuation
        if digits:
            all_characters += string.digits

        random_string = "".join(random.choices(all_characters, k=length))

        return HttpResponse(random_string, status=200)

