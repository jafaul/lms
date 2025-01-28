from django.apps import apps
from django.contrib import admin
from django.conf import settings

User = apps.get_model(settings.AUTH_USER_MODEL)
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "position", "is_staff", "is_superuser", "is_active"]


admin.site.register(User, UserAdmin)
