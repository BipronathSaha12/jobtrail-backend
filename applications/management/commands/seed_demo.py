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

        COMPANIES = [
            "Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "Spotify", "Stripe", "Vercel",
            "Airbnb", "Uber", "Shopify", "GitHub", "GitLab", "Datadog", "Cloudflare", "Atlassian",
            "Figma", "Notion", "Slack", "Canva", "Twilio", "Salesforce", "Adobe", "LinkedIn", "Twitter/X",
            "Oracle", "IBM", "Cisco", "Intel", "AMD", "NVIDIA", "Palantir", "Dropbox", "Square / Block",
            "Coinbase", "Reddit", "Pinterest", "Snap Inc", "Zoom", "DoorDash", "Instacart", "Robinhood",
            "Brain Station 23", "Optimizely", "Chaldal", "Pathao", "Therap (BD) Ltd.", "Kaz Software",
            "Enosis Solutions", "TigerIT", "REVE Systems", "SSL Wireless", "Vivasoft", "Dynamic Solution Innovators",
            "BJIT Limited", "Augmedix BD", "Cefalo Bangladesh", "Kazi IT Center", "Orbitax BD", "LeadSoft",
            "DataSoft Systems", "Inovace Technologies", "Shuttle Technologies", "bKash Limited", "Nagad",
            "Kite Games Studio", "Battery Low Interactive", "Appscode", "NewsCred", "Monstarlab BD"
        ]

        POSITIONS = [
            "Frontend Developer", "Senior Frontend Engineer", "Lead React Architect", "UI/UX Engineer",
            "Backend Engineer", "Senior Backend Developer", "Django / Python Specialist", "Full Stack Developer",
            "Senior Full Stack Engineer", "Staff Software Engineer", "DevOps Engineer", "Site Reliability Engineer (SRE)",
            "Cloud Infrastructure Engineer", "Mobile App Developer (React Native)", "iOS Developer (Swift)",
            "Android Engineer (Kotlin)", "Data Engineer", "Machine Learning Engineer", "AI Solutions Engineer",
            "QA Automation Engineer", "Senior QA Specialist", "Security Engineer", "Application Security Specialist",
            "Solutions Architect", "Technical Lead", "Product Engineer", "API Platform Engineer", "Systems Software Engineer",
            "Junior Software Engineer", "Associate Software Engineer", "Software Engineer II"
        ]

        NOTES_BY_STATUS = {
            "WISHLIST": [
                "Found this vacancy on LinkedIn. Reviewing company culture and preparing tailored CV.",
                "High-priority company. Connecting with team members on LinkedIn for potential referral.",
                "Job description matches my tech stack perfectly (React, TypeScript, Django).",
                "Recommended by peer. Checking Glassdoor reviews and salary benchmarks.",
                "Bookmark for next hiring sprint. Tailoring cover letter emphasizing frontend architecture.",
                "Position opens next week. Following up with recruiter."
            ],
            "APPLIED": [
                "Applied via official career portal with custom portfolio link.",
                "Application submitted through internal employee referral.",
                "Submitted CV and cover letter on Bdjobs / LinkedIn. Confirmation email received.",
                "Applied with customized resume emphasizing full-stack delivery and system design.",
                "Completed candidate questionnaire and submitted GitHub open-source repositories.",
                "Waiting for recruiter screening response."
            ],
            "INTERVIEW": [
                "Passed recruiter call. First technical interview scheduled for Thursday 3:00 PM.",
                "Completed live coding assessment (Data structures & algorithmic problem solving).",
                "System architecture & design interview scheduled with Principal Engineer.",
                "HR and cultural fit interview completed. Awaiting final round schedule.",
                "Take-home coding project submitted. Code review interview booked next week.",
                "Panel interview with Engineering Director and Product Manager completed."
            ],
            "OFFER": [
                "Formal offer letter received! Base salary + performance bonus + stock options.",
                "Offer details: competitive compensation, health insurance, remote work stipend.",
                "Accepted verbal offer! Negotiating start date and signing paperwork.",
                "Offer received with excellent benefits and learning allowance. Deciding by Friday.",
                "Competitive offer in hand. Reviewing contract terms with mentors."
            ],
            "REJECTED": [
                "Position put on hold due to team restructuring.",
                "Role filled internally by existing team member.",
                "Received constructive feedback: strengthen distributed systems experience.",
                "Selected another candidate with more domain-specific background.",
                "Polite rejection received. Invited to re-apply for senior opening next quarter."
            ]
        }

        today = date.today()
        random.seed(42)
        job_types = ["REMOTE", "HYBRID", "ONSITE"]

        # Helper to generate 215 applications for a user
        def generate_user_apps(target_user):
            Application.objects.filter(owner=target_user).delete()
            apps_list = []
            for i in range(215):
                company = COMPANIES[i % len(COMPANIES)]
                position = POSITIONS[(i * 3 + i // len(COMPANIES)) % len(POSITIONS)]
                
                # Realistic status distribution
                if i < 60:
                    status = "WISHLIST"
                elif i < 125:
                    status = "APPLIED"
                elif i < 170:
                    status = "INTERVIEW"
                elif i < 192:
                    status = "OFFER"
                else:
                    status = "REJECTED"

                job_type = job_types[(i + (i % 2)) % len(job_types)]
                days_ago = (i * 2) % 120
                app_date = today - timedelta(days=days_ago)

                salary_base = 50000 + ((i * 3700) % 110000)
                salary = (salary_base // 5000) * 5000

                slug = company.lower().replace(" ", "").replace("/", "").replace("(", "").replace(")", "").replace(".", "")
                job_link = f"https://careers.{slug}.com/jobs/{1000 + i}"
                notes_pool = NOTES_BY_STATUS[status]
                note = notes_pool[i % len(notes_pool)]

                apps_list.append(
                    Application(
                        owner=target_user,
                        company=company,
                        position=position,
                        status=status,
                        job_type=job_type,
                        applied_on=app_date,
                        expected_salary=salary,
                        job_link=job_link,
                        notes=note
                    )
                )
            Application.objects.bulk_create(apps_list)

        generate_user_apps(demo_user)
        self.stdout.write(f"Seeded 215 applications for 'demo'.")

        generate_user_apps(demo_user2)
        self.stdout.write(f"Seeded 215 applications for 'demouser'.")

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

        self.stdout.write(self.style.SUCCESS("All demo admin and client data (215+ jobs) seeded successfully!"))
