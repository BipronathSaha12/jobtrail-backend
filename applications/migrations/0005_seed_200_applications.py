# Generated migration to seed at least 200 job applications for demo users

from django.db import migrations
from datetime import date, timedelta
import random

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

def seed_200_applications(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Application = apps.get_model('applications', 'Application')

    demo_user = User.objects.filter(username='demo').first()
    demouser = User.objects.filter(username='demouser').first()

    targets = [u for u in [demo_user, demouser] if u is not None]
    if not targets:
        return

    today = date.today()
    random.seed(42)  # Deterministic seed for consistency

    statuses = ["WISHLIST", "APPLIED", "INTERVIEW", "OFFER", "REJECTED"]
    job_types = ["REMOTE", "HYBRID", "ONSITE"]

    for user in targets:
        # Clear existing applications to re-seed cleanly with 210 distinct applications
        Application.objects.filter(owner=user).delete()

        apps_to_create = []
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
            
            # Base salary range
            salary_base = 50000 + ((i * 3700) % 110000)
            salary = (salary_base // 5000) * 5000

            slug = company.lower().replace(" ", "").replace("/", "").replace("(", "").replace(")", "").replace(".", "")
            job_link = f"https://careers.{slug}.com/jobs/{1000 + i}"
            notes_pool = NOTES_BY_STATUS[status]
            note = notes_pool[i % len(notes_pool)]

            apps_to_create.append(
                Application(
                    owner=user,
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

        Application.objects.bulk_create(apps_to_create)

class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0004_create_demo_admin'),
    ]

    operations = [
        migrations.RunPython(seed_200_applications),
    ]
