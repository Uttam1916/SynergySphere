from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Project, Task, Membership, Comment

User = get_user_model()

class UserLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class MembershipSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        source="user", queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Membership
        fields = ("id", "project", "user", "user_id", "role", "created_at")
        read_only_fields = ("id", "created_at", "project", "user")

class TaskSerializer(serializers.ModelSerializer):
    assignee = UserLiteSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        source="assignee", queryset=User.objects.all(), write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Task
        fields = (
            "id", "project", "title", "description", "assignee", "assignee_id",
            "due_date", "status", "created_at", "updated_at"
        )
        read_only_fields = ("id", "created_at", "updated_at")

class CommentSerializer(serializers.ModelSerializer):
    author = UserLiteSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "project", "task", "author", "body", "created_at")
        read_only_fields = ("id", "author", "created_at")

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserLiteSerializer(read_only=True)
    memberships = MembershipSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ("id", "name", "description", "owner", "created_at", "updated_at", "memberships", "tasks")
        read_only_fields = ("id", "owner", "created_at", "updated_at")
