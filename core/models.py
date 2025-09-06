from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Project(TimeStamped):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_projects")

    def __str__(self):
        return self.name

class Membership(TimeStamped):
    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("manager", "Manager"),
        ("member", "Member"),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")

    class Meta:
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.user} in {self.project} ({self.role})"

class Task(TimeStamped):
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks"
    )
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"

class Comment(TimeStamped):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="comments")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()

    def __str__(self):
        return f"Comment by {self.author} on {self.project}"
