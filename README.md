# JobTrail - Backend (Django REST Framework)

**JobTrail Backend** is a production-ready, owner-isolated RESTful API service built with Django and Django REST Framework (DRF) powering the JobTrail application tracking platform.

---

## 🔗 Connected Repositories & Deployments

| Component | Repository | Live Deployment URL |
| :--- | :--- | :--- |
| **Frontend (React + Vite)** | [jobtrail-frontend](https://github.com/BipronathSaha12/jobtrail-frontend) | [Live Frontend on Vercel](https://jobtrail-frontend-one.vercel.app/) |
| **Backend (Django REST)** | [jobtrail-backend](https://github.com/BipronathSaha12/jobtrail-backend) | [https://jobtrail-backend-3.onrender.com](https://jobtrail-backend-3.onrender.com) |
| **API Root** | — | [https://jobtrail-backend-3.onrender.com/api/](https://jobtrail-backend-3.onrender.com/api/) |
| **Django Admin Panel** | — | [https://jobtrail-backend-3.onrender.com/admin/](https://jobtrail-backend-3.onrender.com/admin/) |

---

## 🚀 Recent Enhancements & Upgrades

1. **Pre-Seeded 200+ Job Posts (215 Records)**:
   - Migration `0005_seed_200_applications.py` and management command `seed_demo.py` automatically seed **215 realistic job applications** across 70+ global and local tech companies (Google, Meta, Microsoft, Stripe, Vercel, Datadog, Brain Station 23, Optimizely, Chaldal, Pathao, etc.).
   - Balanced across all 5 recruitment stages:
     - 📌 **Wishlist**: 60 jobs (ready for users to apply)
     - 🚀 **Applied**: 65 jobs
     - 📅 **Interview**: 45 jobs
     - 🎉 **Offer**: 22 jobs
     - ❌ **Rejected**: 23 jobs

2. **CSV Export Endpoint**:
   - `GET /api/applications/export/` streams RFC 4180 compliant CSV files with UTF-8 BOM (`\uFEFF`) for seamless opening in Microsoft Excel and spreadsheet tools.
   - Supports query filtering by status (`?status=`), job type (`?job_type=`), and text search (`?search=`).

3. **Monthly Trend Analytics in Stats API**:
   - `GET /api/stats/` provides chronological monthly trend aggregation (`monthly_trends`) powering interactive charts in the frontend.

4. **Dynamic Pagination**:
   - Added `ApplicationPagination` supporting `?page_size=` query parameter (up to 500 records per page) to seamlessly support both the standard 10-item paginated list and high-volume Kanban pipeline views.

5. **Automatic Production Migration & Seeding**:
   - Updated `Procfile` and `render.yaml` to run `python manage.py migrate && python manage.py seed_demo && gunicorn ...` on container startup, ensuring demo accounts and data exist on ephemeral containers.

---

## 🛠️ Tech Stack
- **Language**: Python 3.10+ / 3.14
- **Framework**: Django 5.x / 6.x
- **API Toolkit**: Django REST Framework (DRF)
- **Authentication**: JWT via `djangorestframework-simplejwt`
- **CORS Handling**: `django-cors-headers`
- **Filtering**: `django-filter`
- **WSGI Server**: `gunicorn`
- **Database**: SQLite (local) / PostgreSQL ready

---

## 🔐 Demo Accounts & Credentials

| Role | Username | Password | Access Portal | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Superuser / Staff** | `admin` | `admin123` | `/admin/` | Full Django Admin management access |
| **Job Seeker Demo** | `demo` | `demo123` | `/login` (Frontend) | Pre-seeded with 215 applications across all stages |
| **Secondary Demo User** | `demouser` | `password123` | `/login` (Frontend) | Pre-seeded with 215 applications |
| **Owner Isolation Tester** | `testuser2` | `password123` | `/login` (Frontend) | Verifies user isolation (returns 404 for User A items) |

---

## 📡 API Endpoints Specification

| Method | Endpoint | Auth | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/register/` | Public | Register new user account (`username`, `email`, `password`) |
| `POST` | `/api/login/` | Public | Authenticate user (Username or Email) & get JWT `access` and `refresh` tokens |
| `POST` | `/api/token/refresh/` | Public | Refresh expired JWT access token |
| `GET` | `/api/stats/` | Bearer Token | Aggregated status counts (`wishlist`, `applied`, `interview`, `offer`, `rejected`, `total`) and chronological `monthly_trends` |
| `GET` | `/api/applications/` | Bearer Token | Paginated application list (supports `?search=`, `?status=`, `?job_type=`, `?page=`, `?page_size=`, `?ordering=`) |
| `POST` | `/api/applications/` | Bearer Token | Create new job application (auto-assigns owner) |
| `GET` | `/api/applications/<id>/` | Bearer Token | Application detail by ID (strict owner isolation; 404 for unauthorized items) |
| `PUT / PATCH`| `/api/applications/<id>/` | Bearer Token | Update application status or details |
| `DELETE` | `/api/applications/<id>/` | Bearer Token | Delete application record |
| `GET` | `/api/applications/export/` | Bearer Token | Download application records as CSV spreadsheet attachment |

---

## 🚀 Setup & Local Execution

1. **Clone repository**:
   ```bash
   git clone https://github.com/BipronathSaha12/jobtrail-backend.git
   cd jobtrail-backend
   ```

2. **Create & activate virtual environment**:
   ```bash
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**:
   ```bash
   cp .env.example .env
   ```

5. **Run migrations & seed demo data**:
   ```bash
   python manage.py migrate
   python manage.py seed_demo
   ```

6. **Start development server**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
   API is accessible at `http://127.0.0.1:8000/`.

---

## 🧪 Unit Tests
Run the automated test suite covering authentication, owner isolation (404), filtering, and statistics:
```bash
python manage.py test applications
```
