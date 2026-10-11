from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from applications.models import Application
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = "Seeds demo admin superusers and client-side demo users with rich applications"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding demo admin and client accounts...")

        # 1. Create/update primary Admin superuser for Django Admin Panel (/admin/)
        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@jobtrail.com", "is_staff": True, "is_superuser": True}
        )
        admin_user.set_password("admin123")
        admin_user.email = "admin@jobtrail.com"
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save()
        self.stdout.write(self.style.SUCCESS("Demo Admin superuser created/ready: admin / admin123"))

        # Also ensure 'Admin' alias works
        admin_alias, _ = User.objects.get_or_create(
            username="Admin",
            defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True}
        )
        admin_alias.set_password("admin123")
        admin_alias.is_staff = True
        admin_alias.is_superuser = True
        admin_alias.is_active = True
        admin_alias.save()

        # 2. Create/update primary client-side demo user 'demo' for Web UI (/login)
        demo_user, _ = User.objects.get_or_create(
            username="demo",
            defaults={"email": "demo@jobtrail.com"}
        )
        demo_user.set_password("demo123")
        demo_user.email = "demo@jobtrail.com"
        demo_user.is_active = True
        demo_user.save()
        self.stdout.write(self.style.SUCCESS("Demo Client user created/ready: demo / demo123"))

        # 3. Create/update secondary demo user 'demouser'
        demo_user2, _ = User.objects.get_or_create(
            username="demouser",
            defaults={"email": "demouser@jobtrail.com"}
        )
        demo_user2.set_password("password123")
        demo_user2.email = "demouser@jobtrail.com"
        demo_user2.is_active = True
        demo_user2.save()

        # 4. Create user for owner isolation testing
        isolation_user, _ = User.objects.get_or_create(
            username="testuser2",
            defaults={"email": "user2@jobtrail.com"}
        )
        isolation_user.set_password("password123")
        isolation_user.is_active = True
        isolation_user.save()

        # Rich sample application data spanning all 5 statuses
        sample_jobs = [
            ("Brain Station 23", "Senior Frontend Developer", Application.StatusChoices.INTERVIEW, Application.JobTypeChoices.REMOTE, 75000, "Referred by senior engineer. System design interview scheduled."),
            ("Google", "Software Engineer - UI", Application.StatusChoices.APPLIED, Application.JobTypeChoices.HYBRID, 160000, "Applied directly via Google Careers portal."),
            ("Optimizely", "Full Stack Engineer", Application.StatusChoices.INTERVIEW, Application.JobTypeChoices.REMOTE, 85000, "Passed technical coding round."),
            ("Chaldal", "Lead Frontend Architect", Application.StatusChoices.OFFER, Application.JobTypeChoices.ONSITE, 95000, "Formal offer received with stock options."),
            ("Meta", "React Frontend Engineer", Application.StatusChoices.APPLIED, Application.JobTypeChoices.REMOTE, 150000, "Submitted portfolio and resume via referral."),
            ("Pathao", "Senior Frontend Engineer", Application.StatusChoices.REJECTED, Application.JobTypeChoices.ONSITE, 65000, "Position put on freeze for Q4."),
            ("Netflix", "UI Platform Engineer", Application.StatusChoices.WISHLIST, Application.JobTypeChoices.REMOTE, 175000, "Customizing resume for upcoming role opening."),
            ("Stripe", "Design Engineer", Application.StatusChoices.OFFER, Application.JobTypeChoices.REMOTE, 145000, "Offer received! Negotiating start date."),
            ("Therap (BD) Ltd.", "Software Engineer II", Application.StatusChoices.WISHLIST, Application.JobTypeChoices.ONSITE, 70000, "Reviewing requirements and reach-out contacts."),
            ("Kaz Software", "Django & React Specialist", Application.StatusChoices.APPLIED, Application.JobTypeChoices.HYBRID, 60000, "Submitted code samples and GitHub link."),
            ("Enosis Solutions", "Senior Software Engineer", Application.StatusChoices.INTERVIEW, Application.JobTypeChoices.ONSITE, 72000, "Panel interview on Monday afternoon."),
            ("Vercel", "Frontend Developer", Application.StatusChoices.WISHLIST, Application.JobTypeChoices.REMOTE, 130000, "Preparing open-source contributions for outreach."),
            ("TigerIT", "Python & Django Engineer", Application.StatusChoices.APPLIED, Application.JobTypeChoices.ONSITE, 68000, "Applied via Bdjobs listing."),
            ("REVE Systems", "System & Software Engineer", Application.StatusChoices.REJECTED, Application.JobTypeChoices.ONSITE, 50000, "Selected an internal candidate."),
            ("SSL Wireless", "Full Stack Web Engineer", Application.StatusChoices.APPLIED, Application.JobTypeChoices.REMOTE, 62000, "Completed online technical assessment."),
            ("Vivasoft", "React / Node.js Developer", Application.StatusChoices.INTERVIEW, Application.JobTypeChoices.HYBRID, 68000, "Passed HR screening, preparing for live coding.")
        ]

        today = date.today()

        # Seed applications for 'demo'
        Application.objects.filter(owner=demo_user).delete()
        for idx, (company, pos, status_val, jtype, salary, notes) in enumerate(sample_jobs):
            app_date = today - timedelta(days=idx * 2)
            Application.objects.create(
                owner=demo_user,
                company=company,
                position=pos,
                status=status_val,
                job_type=jtype,
                applied_on=app_date,
                expected_salary=salary,
                job_link=f"https://careers.{company.lower().replace(' ', '').replace('(', '').replace(')', '').replace('.', '')}.com",
                notes=notes
            )
        self.stdout.write(f"Seeded {len(sample_jobs)} applications for 'demo'.")

        # Seed applications for 'demouser'
        Application.objects.filter(owner=demo_user2).delete()
        for idx, (company, pos, status_val, jtype, salary, notes) in enumerate(sample_jobs):
            app_date = today - timedelta(days=idx * 2)
            Application.objects.create(
                owner=demo_user2,
                company=company,
                position=pos,
                status=status_val,
                job_type=jtype,
                applied_on=app_date,
                expected_salary=salary,
                job_link=f"https://careers.{company.lower().replace(' ', '').replace('(', '').replace(')', '').replace('.', '')}.com",
                notes=notes
            )
        self.stdout.write(f"Seeded {len(sample_jobs)} applications for 'demouser'.")

        # Seed 1 isolated application for testuser2
        Application.objects.filter(owner=isolation_user).delete()
        Application.objects.create(
            owner=isolation_user,
            company="Confidential Aerospace",
            position="Cybersecurity Analyst",
            status=Application.StatusChoices.WISHLIST,
            job_type=Application.JobTypeChoices.REMOTE,
            expected_salary=90000,
            notes="Confidential test application belonging only to testuser2."
        )

        self.stdout.write(self.style.SUCCESS("All demo admin and client data seeded successfully!"))
