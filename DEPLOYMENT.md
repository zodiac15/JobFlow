# Deployment Guide - Job Search App

This guide provides instructions for deploying the Job Search application to production.

## Prerequisites

- Python 3.8+
- Node.js 16+
- A production database (PostgreSQL recommended, or SQLite for small deployments)
- A domain name (optional but recommended)

## Environment Variables

### Backend Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```bash
# Flask Configuration
SECRET_KEY=your-production-secret-key-here  # Generate a strong random key
FLASK_DEBUG=False

# API Keys
GEMINI_API_KEY=your-gemini-api-key

# Database (optional - defaults to SQLite)
# For PostgreSQL:
# DATABASE_URL=postgresql://username:password@host:port/database
# For SQLite (default):
DATABASE_URL=sqlite:///jobs.db

# CORS Origins (comma-separated list of allowed frontend URLs)
CORS_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com
```

### Frontend Environment Variables

Create a `.env` file in the `frontend/` directory:

```bash
# API Base URL - Point to your backend server
VITE_API_BASE_URL=https://your-api-domain.com
```

## Backend Deployment

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 3. Run with Gunicorn (Production Server)

```bash
# Basic command
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With more workers and timeout
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app

# With logging
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - --error-logfile - app:app
```

**Note for Windows**: Gunicorn doesn't work on Windows. Use `waitress` instead:

```bash
pip install waitress
waitress-serve --port=5000 app:app
```

### 4. Using a Process Manager (Recommended)

For production, use a process manager like `systemd`, `supervisor`, or `pm2`:

**Example systemd service** (`/etc/systemd/system/jobflow-backend.service`):

```ini
[Unit]
Description=JobFlow Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/job-search-app/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## Frontend Deployment

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Build for Production

```bash
npm run build
```

This creates a `dist/` folder with optimized static files.

### 3. Serve Static Files

You can serve the `dist/` folder using:

- **Nginx** (recommended)
- **Apache**
- **Vercel** (easiest for static sites)
- **Netlify**
- **AWS S3 + CloudFront**

**Example Nginx Configuration**:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /path/to/job-search-app/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Optional: Proxy API requests to backend
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Platform-Specific Deployment

### Deploying to Vercel (Frontend)

1. Install Vercel CLI: `npm i -g vercel`
2. Navigate to frontend: `cd frontend`
3. Run: `vercel`
4. Set environment variable in Vercel dashboard: `VITE_API_BASE_URL`

### Deploying to Heroku (Backend)

1. Create `Procfile` in backend directory:
   ```
   web: gunicorn app:app
   ```

2. Create `runtime.txt`:
   ```
   python-3.11.0
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set GEMINI_API_KEY=your-api-key
   git push heroku main
   ```

### Deploying to Railway

1. Connect your GitHub repository
2. Add environment variables in Railway dashboard
3. Railway will auto-detect and deploy both frontend and backend

## Security Checklist

- [ ] `FLASK_DEBUG` is set to `False` in production
- [ ] Strong `SECRET_KEY` is generated and set
- [ ] `.env` files are NOT committed to Git (verify with `.gitignore`)
- [ ] CORS origins are restricted to your frontend domain(s)
- [ ] HTTPS is enabled (use Let's Encrypt for free SSL)
- [ ] Database credentials are secure
- [ ] API keys are kept secret

## Database Migration (SQLite to PostgreSQL)

If you want to migrate from SQLite to PostgreSQL:

1. Export SQLite data:
   ```bash
   sqlite3 jobs.db .dump > backup.sql
   ```

2. Update `DATABASE_URL` in `.env` to PostgreSQL connection string

3. Initialize PostgreSQL database:
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

4. Import data (may require manual conversion)

## Monitoring and Logs

- Use application monitoring tools like Sentry, DataDog, or New Relic
- Set up log aggregation (e.g., Papertrail, Loggly)
- Monitor server resources (CPU, memory, disk)

## Troubleshooting

### CORS Errors
- Verify `CORS_ORIGINS` includes your frontend domain
- Check that credentials are being sent from frontend

### Database Connection Issues
- Verify `DATABASE_URL` format
- Check database server is running and accessible
- Ensure firewall allows connections

### Build Failures
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Clear build cache: `rm -rf dist`

## Support

For issues or questions, refer to the main README or create an issue in the repository.
