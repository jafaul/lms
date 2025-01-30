from django.contrib import admin

from apps.management.models import Course, Task, Lecture


class LectureInline(admin.TabularInline):
    model = Lecture
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = (LectureInline, )
    list_display = ("title", "description")
    search_fields = ("title",)
    list_filter = ("title",)
    readonly_fields = ("title", "description", )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "max_mark", "deadline")
    search_fields = ("title", )
    list_filter = ("title", )
    readonly_fields = ("title", "max_mark", )


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title", )
    list_filter = ("title", )
    readonly_fields = ("title", )
