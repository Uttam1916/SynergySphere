from django.contrib import admin
from .models import Project, Task

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Message)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")
    search_fields = ("name", "description")

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "assignee", "due_date", "created_at")
    list_filter = ("status", "due_date")
    search_fields = ("title", "description")
