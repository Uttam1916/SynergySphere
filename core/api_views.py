from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Project, Task, Membership, Comment

from .serializers import (
    ProjectSerializer, TaskSerializer, MembershipSerializer, CommentSerializer, UserLiteSerializer
)

from .permissions import IsProjectMember

User = get_user_model()

class MeViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLiteSerializer

    def get_object(self):
        return self.request.user

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(owner=user) | Q(memberships__user=user)
        ).distinct().order_by("-created_at")

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        # owner auto-membership
        Membership.objects.get_or_create(project=project, user=self.request.user, defaults={"role": "owner"})

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(project__owner=user) | Q(project__memberships__user=user)
        ).distinct().order_by("-created_at")

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(
            Q(project__owner=user) | Q(project__memberships__user=user)
        ).distinct().order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class MembershipViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
        """
        List project members, add or remove them.
        Create: POST with { "project": <id>, "user_id": <id>, "role": "member" }
        """
        serializer_class = MembershipSerializer
        permission_classes = [IsAuthenticated, IsProjectMember]

        def get_queryset(self):
            user = self.request.user
            return Membership.objects.filter(
                Q(project__owner=user) | Q(project__memberships__user=user)
            ).select_related("project", "user").distinct()
