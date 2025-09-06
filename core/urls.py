from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProjectViewSet, TaskViewSet, CommentViewSet, MembershipViewSet, MeViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"memberships", MembershipViewSet, basename="membership")
router.register(r"me", MeViewSet, basename="me")

urlpatterns = [
    path("", include(router.urls)),
]
