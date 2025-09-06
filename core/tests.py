from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Project, Membership

User = get_user_model()

class ProjectApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="testpass123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_project(self):
        payload = {"name": "My First Project", "description": "Test project"}
        res = self.client.post("/api/projects/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.name, payload["name"])
        # owner auto-added to membership
        self.assertTrue(Membership.objects.filter(project=project, user=self.user).exists())

    def test_list_projects(self):
        Project.objects.create(name="P1", description="", owner=self.user)
        Project.objects.create(name="P2", description="", owner=self.user)
        res = self.client.get("/api/projects/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 2)
