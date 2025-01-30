from django.contrib import admin

from apps.assessment.models import Response, Mark


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):

    list_display = ('id', 'description')
    search_fields = ('id', 'description')
    list_filter = ('description', "submission_datetime")
    list_per_page = 10
    readonly_fields = ('id', "submission_datetime")


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'mark_value')
    search_fields = ('id', 'mark_value')
    list_filter = ('mark_value', "submission_datetime")
    list_per_page = 10
    readonly_fields = ("id", 'mark_value', "submission_datetime")
