from rest_framework.permissions import BasePermission

class IsProjectMember(BasePermission):
    """
    Only members of a project (or superusers) can access its resources.
    """

    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True

        project = getattr(obj, "project", None)
        if project is None and hasattr(view, "get_project"):
            project = view.get_project(obj)
        if project is None and hasattr(obj, "id"):  # if obj *is* a project
            project = obj

        if not project:
            return False

        return project.owner_id == user.id or project.memberships.filter(user=user).exists()
