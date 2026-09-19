# JobTrail - Backend (Django REST Framework)

**JobTrail Backend** is a private, owner-scoped RESTful API service built with Django 5 and Django REST Framework (DRF) for tracking job application workflows.

---

## 🔗 Related Repositories
- **Frontend Repository**: [JobTrail Frontend (React + Vite)](https://github.com/YOUR_GITHUB_USERNAME/jobtrail-frontend)

---

## 🛠️ Tech Stack
- **Python**: 3.10+
- **Django**: 5.x / 4.2+
- **Django REST Framework (DRF)**: Web API toolkit
- **JWT Auth**: `djangorestframework-simplejwt`
- **CORS**: `django-cors-headers`
- **Filtering**: `django-filter`
- **Database**: SQLite (`db.sqlite3`)
- **Environment Management**: `python-decouple`

---

## 🚀 Setup & Local Execution

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   # Windows (Git Bash / PowerShell)
   python -m venv venv
   source venv/Scripts/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Seed Demo Data & Admin Superuser**:
   Populates test users (`demouser` / `password123`, `Admin` / `admin`, and `testuser2` / `password123`) and sample job applications:
   ```bash
   python manage.py seed_demo
   ```

7. **Run Server**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
   The API server will run live on `http://127.0.0.1:8000/`.

---

## 🔑 Environment Variables (`.env`)

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | `django-insecure-...` | Secret key for Django cryptographic signing |
| `DEBUG` | `True` | Debug mode switch |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | Comma-separated allowed hostnames |

---

## 📡 API Endpoints Table

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/register/` | Public | Register new user account (`username`, `email`, `password`) |
| `POST` | `/api/login/` | Public | Authenticate user (by Username or Email) & return JWT `access` and `refresh` tokens |
| `POST` | `/api/token/refresh/` | Public | Refresh expired JWT access token |
| `GET` | `/api/stats/` | Bearer Token | Get user's aggregated status counts (`total`, `wishlist`, `applied`, `interview`, `offer`, `rejected`) |
| `GET` | `/api/applications/` | Bearer Token | Get paginated list of user's own applications (supports `?search=`, `?status=`, `?job_type=`, `?ordering=`) |
| `POST` | `/api/applications/` | Bearer Token | Create new job application (owner auto-assigned from token) |
| `GET` | `/api/applications/<id>/` | Bearer Token | Get application detail by ID (returns 404 for other users' records) |
| `PUT / PATCH` | `/api/applications/<id>/` | Bearer Token | Update application details |
| `DELETE` | `/api/applications/<id>/` | Bearer Token | Delete application record |

---

## 🧪 Unit Tests
Run backend test suite covering authentication, owner isolation (404), filtering, and statistics:
```bash
python manage.py test applications
```
