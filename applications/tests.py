from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Application

class JobTrailBackendTests(APITestCase):
    def setUp(self):
        # Create two distinct users
        self.user_a = User.objects.create_user(
            username="user_a",
            email="usera@example.com",
            password="password123"
        )
        self.user_b = User.objects.create_user(
            username="user_b",
            email="userb@example.com",
            password="password123"
        )

        # Create applications for user_a
        self.app_a1 = Application.objects.create(
            owner=self.user_a,
            company="Brain Station 23",
            position="Frontend Developer",
            status=Application.StatusChoices.INTERVIEW,
            job_type=Application.JobTypeChoices.REMOTE,
            expected_salary=45000
        )
        self.app_a2 = Application.objects.create(
            owner=self.user_a,
            company="Optimizely",
            position="Backend Engineer",
            status=Application.StatusChoices.APPLIED,
            job_type=Application.JobTypeChoices.HYBRID
        )

        # Create application for user_b
        self.app_b1 = Application.objects.create(
            owner=self.user_b,
            company="Secret Corp",
            position="Security Engineer",
            status=Application.StatusChoices.OFFER,
            job_type=Application.JobTypeChoices.ONSITE
        )

    def test_user_registration(self):
        """Test POST /api/register/ creates user and hides password"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword"
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)
        self.assertEqual(response.data["username"], "newuser")

    def test_user_login(self):
        """Test POST /api/login/ returns JWT access and refresh tokens"""
        data = {
            "username": "user_a",
            "password": "password123"
        }
        response = self.client.post("/api/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_owner_isolation_returns_404(self):
        """Test User B trying to access User A's application returns 404 (not 403 or data)"""
        self.client.force_authenticate(user=self.user_b)
        response = self.client.get(f"/api/applications/{self.app_a1.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_status_filter_and_search(self):
        """Test status filtering and text searching"""
        self.client.force_authenticate(user=self.user_a)
        
        # Test status filter
        response = self.client.get("/api/applications/?status=INTERVIEW")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["company"], "Brain Station 23")

        # Test search filter
        response = self.client.get("/api/applications/?search=Backend")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["position"], "Backend Engineer")

    def test_stats_endpoint(self):
        """Test GET /api/stats/ returns exact stats for logged in user"""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get("/api/stats/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total"], 2)
        self.assertEqual(response.data["interview"], 1)
        self.assertEqual(response.data["applied"], 1)
        self.assertEqual(response.data["wishlist"], 0)
        self.assertEqual(response.data["offer"], 0)
        self.assertEqual(response.data["rejected"], 0)

    def test_unauthenticated_requests_return_401(self):
        """Test request without token returns 401 Unauthorized"""
        response = self.client.get("/api/applications/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
