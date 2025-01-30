from django.apps import apps
from django.contrib import admin
from django.conf import settings
# Register your models here.

User = apps.get_model(settings.AUTH_USER_MODEL)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("position", "first_name", "last_name",  "email", "position", "is_staff")
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("date_joined", "last_name", "position")
    list_per_page = 15
