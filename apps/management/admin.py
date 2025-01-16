from django.contrib import admin

from apps.management.models import Course, Task, Lecture


# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description"]

#
# class CourseStudentAdmin(admin.ModelAdmin):
#     list_display = ["id", "course", "student"]
#

class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "max_mark", "deadline"]


class LectureAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description"]


admin.site.register(Course, CourseAdmin)
# admin.site.register(CourseStudent, CourseStudentAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Lecture, LectureAdmin)