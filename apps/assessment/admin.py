from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from apps.assessment.models import Response, Mark


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    search_fields = ('id', 'description')
    list_filter = ('description', "submission_datetime")
    list_per_page = 10
    readonly_fields = ('id', "submission_datetime")

    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE(attrs={"rows": 3, "cols": 20}),
        }
    }


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'mark_value')
    search_fields = ('id', 'mark_value')
    list_filter = ('mark_value', "submission_datetime")
    list_per_page = 10
    readonly_fields = ("id", 'mark_value', "submission_datetime")
