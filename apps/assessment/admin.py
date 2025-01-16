from django.contrib import admin

from apps.assessment.models import Response, Mark


# Register your models here.
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')


class MarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'mark_value')


admin.site.register(Response, ResponseAdmin)
admin.site.register(Mark, MarkAdmin)
