
from django.shortcuts import render, get_object_or_404
from .models import Project


def dashboard(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, "core/dashboard.html", {"projects": projects})


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    tasks = project.tasks.all()
    return render(request, "core/project_detail.html", {"project": project, "tasks": tasks})
