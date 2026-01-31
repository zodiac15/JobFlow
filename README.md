# JobFlow - AI-Powered Job Search Platform

<div align="center">

![JobFlow](https://img.shields.io/badge/JobFlow-Job%20Search%20Platform-6366f1?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A modern, full-stack job search application with AI-powered resume generation, application tracking, and multi-platform job scraping.**

[Features](#features) • [Demo](#demo) • [Installation](#installation) • [Usage](#usage) • [Deployment](#deployment) • [Contributing](#contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

**JobFlow** is a comprehensive job search platform that aggregates job listings from multiple sources (LinkedIn, Naukri, Instahyre, WeWorkRemotely, and more), provides AI-powered resume and cover letter generation, and helps you track your applications—all in one beautiful, modern interface.

### Why JobFlow?

- 🔍 **Multi-Platform Search**: Scrape jobs from 5+ major job boards simultaneously
- 🤖 **AI-Powered Tools**: Generate tailored resumes and cover letters using Google Gemini AI
- 📊 **Application Tracker**: Keep track of all your applications in one place
- 🎨 **Modern UI**: Beautiful, responsive design with Tailwind CSS and Vue 3
- 🔐 **Secure**: Built-in authentication, CSRF protection, and rate limiting
- 🚀 **Production Ready**: Environment-based configuration and deployment guides

---

## ✨ Features

### Core Features

#### 🔎 Job Aggregation
- **Multi-source scraping**: LinkedIn, Naukri, Instahyre, Foundit, WeWorkRemotely
- **Smart filtering**: Search by title, location, and keywords
- **Auto-refresh**: Automatically scrapes new jobs when listings are stale
- **Duplicate detection**: Prevents duplicate job listings

#### 👤 User Management
- **Authentication**: Secure login/registration with password hashing
- **User profiles**: Manage personal information, skills, experience, and education
- **Resume upload**: Upload and parse PDF/DOCX resumes
- **Admin panel**: User management and job moderation

#### 🤖 AI-Powered Tools
- **Resume Generator**: Create tailored resumes based on job descriptions using Gemini AI
- **Cover Letter Generator**: Generate personalized cover letters
- **CV Parser**: Extract information from uploaded resumes

#### 📈 Application Tracking
- **Status tracking**: Track applications through stages (Applied, Interviewing, Offer, Rejected)
- **Notes**: Add notes to each application
- **Timeline view**: See your application history at a glance

#### 💾 Job Management
- **Save jobs**: Bookmark interesting positions
- **Job details**: View full job descriptions and requirements
- **Direct apply**: Quick links to original job postings

### Security Features
- ✅ CSRF protection with Flask-WTF
- ✅ Rate limiting to prevent abuse
- ✅ Secure session cookies (HttpOnly, SameSite)
- ✅ Password hashing with Werkzeug
- ✅ Environment-based secrets management

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 2.x
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Authentication**: Flask-Login
- **Security**: Flask-WTF (CSRF), Flask-Limiter (Rate Limiting)
- **Web Scraping**: BeautifulSoup4, Selenium
- **AI**: Google Generative AI (Gemini)
- **Server**: Gunicorn (Production)

### Frontend
- **Framework**: Vue.js 3 (Composition API)
- **Routing**: Vue Router 4
- **Styling**: Tailwind CSS 3
- **Build Tool**: Vite 4
- **Animations**: FormKit Auto-Animate
- **Markdown**: Marked, DOMPurify
- **Testing**: Vitest

### DevOps
- **Version Control**: Git
- **Environment**: python-dotenv
- **Testing**: pytest (Backend), Vitest (Frontend)

---

## 🏗️ Architecture

```
job-search-app/
├── backend/                 # Flask API server
│   ├── app.py              # Main application entry point
│   ├── models.py           # SQLAlchemy models (User, Job, Application)
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment variables template
│   ├── routes/             # API route blueprints
│   │   ├── ai_routes.py    # AI-powered features
│   │   ├── admin_routes.py # Admin panel endpoints
│   │   └── seo_routes.py   # SEO and sitemap
│   ├── scrapers/           # Job scraping modules
│   │   ├── base_scraper.py
│   │   ├── linkedin.py
│   │   ├── naukri.py
│   │   ├── instahyre.py
│   │   ├── foundit.py
│   │   └── weworkremotely.py
│   ├── utils/              # Utility functions
│   │   └── cv_parser.py    # Resume parsing
│   └── tests/              # Backend tests
│
├── frontend/               # Vue.js SPA
│   ├── src/
│   │   ├── main.js         # App entry point
│   │   ├── App.vue         # Root component
│   │   ├── router/         # Vue Router configuration
│   │   ├── views/          # Page components
│   │   │   ├── HomeView.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── RegisterView.vue
│   │   │   ├── UserProfileView.vue
│   │   │   ├── TrackerView.vue
│   │   │   ├── SavedJobsView.vue
│   │   │   └── Admin*.vue
│   │   ├── components/     # Reusable components
│   │   │   ├── Navbar.vue
│   │   │   ├── JobCard.vue
│   │   │   ├── ResumeGeneratorModal.vue
│   │   │   └── CoverLetterModal.vue
│   │   └── utils/          # Frontend utilities
│   │       └── api.js      # API client with CSRF
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .env.example
│
├── .gitignore              # Git ignore rules
├── DEPLOYMENT.md           # Deployment guide
└── README.md               # This file
```

---

## 🚀 Installation

### Prerequisites

- **Python** 3.8 or higher
- **Node.js** 16 or higher
- **npm** or **yarn**
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/job-search-app.git
cd job-search-app
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env and add your API keys
# Required: GEMINI_API_KEY, SECRET_KEY
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create .env file from example
cp .env.example .env

# Edit .env if needed (default: http://localhost:5000)
```

### 4. Initialize Database

```bash
# From backend directory
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

---

## ⚙️ Configuration

### Backend Environment Variables

Create `backend/.env`:

```bash
# Flask Configuration
SECRET_KEY=your-super-secret-key-here
FLASK_DEBUG=True

# API Keys
GEMINI_API_KEY=your-gemini-api-key

# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite:///jobs.db

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:5173,http://localhost:5174
```

### Frontend Environment Variables

Create `frontend/.env`:

```bash
# API Base URL
VITE_API_BASE_URL=http://localhost:5000
```

### Getting API Keys

- **Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

---

## 💻 Usage

### Development Mode

#### Start Backend Server

```bash
cd backend
python app.py
```

Server runs on: `http://localhost:5000`

#### Start Frontend Dev Server

```bash
cd frontend
npm run dev
```

Frontend runs on: `http://localhost:5173`

### Production Mode

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production deployment instructions.

---

## 📡 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |
| POST | `/api/auth/logout` | Logout user |
| GET | `/api/auth/me` | Get current user |

### Job Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs` | Get all jobs (with filters) |
| GET | `/api/jobs/:id` | Get job by ID |
| POST | `/api/scrape` | Trigger job scraping |

### User Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/user/profile` | Get user profile |
| POST | `/api/user/profile` | Update user profile |
| POST | `/api/user/saved-jobs/:id` | Toggle save job |
| GET | `/api/user/saved-jobs` | Get saved jobs |
| GET | `/api/user/applications` | Get applications |
| POST | `/api/user/applications` | Create application |
| PUT | `/api/user/applications/:id` | Update application |
| DELETE | `/api/user/applications/:id` | Delete application |

### AI Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai/generate-resume` | Generate resume |
| POST | `/api/ai/generate-cover-letter` | Generate cover letter |
| POST | `/api/parse-cv` | Parse uploaded CV |

### Admin Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/users` | Get all users |
| DELETE | `/api/admin/users/:id` | Delete user |
| GET | `/api/admin/jobs` | Get all jobs |
| DELETE | `/api/admin/jobs/:id` | Delete job |
| GET | `/api/admin/stats` | Get dashboard stats |

---

## 🌐 Deployment

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Quick Deploy Options

- **Frontend**: Vercel, Netlify, AWS S3 + CloudFront
- **Backend**: Heroku, Railway, DigitalOcean, AWS EC2
- **Full Stack**: Railway, Render, Fly.io

### Production Checklist

- [ ] Set `FLASK_DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `CORS_ORIGINS` for your domain
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set up monitoring and logging
- [ ] Configure backups

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript/Vue code
- Write tests for new features
- Update documentation as needed

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Job boards: LinkedIn, Naukri, Instahyre, Foundit, WeWorkRemotely
- Google Gemini AI for resume generation
- Vue.js and Flask communities
- All contributors and users

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

<div align="center">

**Made with ❤️ by the JobFlow Team**

⭐ Star this repo if you find it helpful!

</div>
