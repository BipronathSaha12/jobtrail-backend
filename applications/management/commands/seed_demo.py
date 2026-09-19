from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from applications.models import Application
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = "Seeds demo users and applications for testing"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding demo data...")

        # Create Admin superuser for Django Admin portal
        admin_user, _ = User.objects.get_or_create(
            username="Admin",
            defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True}
        )
        admin_user.set_password("admin")
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        self.stdout.write("Created/updated Admin superuser: Admin / admin")

        # Create demo user 1
        user1, created1 = User.objects.get_or_create(
            username="demouser",
            defaults={"email": "demo@example.com"}
        )

        if created1:
            user1.set_password("password123")
            user1.save()
            self.stdout.write(f"Created demo user: demouser / password123")
        else:
            self.stdout.write("Demo user demouser already exists.")

        # Create demo user 2 for isolation testing
        user2, created2 = User.objects.get_or_create(
            username="testuser2",
            defaults={"email": "user2@example.com"}
        )
        if created2:
            user2.set_password("password123")
            user2.save()
            self.stdout.write(f"Created second user: testuser2 / password123")

        # Sample application data for user1
        sample_jobs = [
            ("Brain Station 23", "Frontend Developer", Application.StatusChoices.INTERVIEW, Application.JobTypeChoices.REMOTE, 45000, "Referred by Rafi."),
            ("Optimizely", "Backend Engineer", Application.StatusChoices.APPLIED, Application.JobTypeChoices.HYBRID, 60000, "Applied via LinkedIn"),
            ("Chaldal", "Full Stack Engineer", Application.StatusChoices.OFFER, Application.JobTypeChoices.ONSITE, 55000, "Got offer letter!"),
            ("Pathao", "React Developer", Application.StatusChoices.REJECTED, Application.JobTypeChoices.REMOTE, 40000, "Resume screened out"),
            ("Therapbd", "Software Engineer", Application.StatusChoices.WISHLIST, Application.JobTypeChoices.ONSITE, 50000, "Preparing CV"),
            ("Kaz Software", "Django Developer", Application.StatusChoices.APPLIED, Application.JobTypeChoices.HYBRID, 48000, "Submitted application"),
            ("Enosis Solutions", "Software Engineer I", Application.StatusChoices.INTERVIEW, Application.JobTypeChoices.ONSITE, 52000, "Technical interview on Tuesday"),
            ("TigerIT", "Python Developer", Application.StatusChoices.WISHLIST, Application.JobTypeChoices.REMOTE, 55000, "Check position details"),
            ("REVE Systems", "System Engineer", Application.StatusChoices.REJECTED, Application.JobTypeChoices.ONSITE, 38000, "Position closed"),
            ("SSL Wireless", "Fullstack Developer", Application.StatusChoices.APPLIED, Application.JobTypeChoices.REMOTE, 47000, "Applied on company portal"),
            ("Dynamic Solution Innovators", "Junior Software Engineer", Application.StatusChoices.OFFER, Application.JobTypeChoices.ONSITE, 42000, "Accepted offer"),
            ("Vivasoft", "Frontend Engineer", Application.StatusChoices.INTERVIEW, Application.JobTypeChoices.HYBRID, 50000, "System Design round"),
        ]

        # Clear existing applications for user1 to prevent duplicates during re-seeding
        Application.objects.filter(owner=user1).delete()

        today = date.today()
        for idx, (company, pos, status, jtype, salary, notes) in enumerate(sample_jobs):
            app_date = today - timedelta(days=idx * 2)
            Application.objects.create(
                owner=user1,
                company=company,
                position=pos,
                status=status,
                job_type=jtype,
                applied_on=app_date,
                expected_salary=salary,
                job_link=f"https://{company.lower().replace(' ', '')}.com/careers/{idx+1}",
                notes=notes
            )

        # Seed 1 application for user2 to test owner isolation
        Application.objects.filter(owner=user2).delete()
        Application.objects.create(
            owner=user2,
            company="Secret Corp",
            position="Private Specialist",
            status=Application.StatusChoices.WISHLIST,
            job_type=Application.JobTypeChoices.REMOTE,
            notes="Belongs strictly to testuser2"
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded demo data!"))
