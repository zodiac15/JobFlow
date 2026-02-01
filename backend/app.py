from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db, Job, User, SavedJob, Application
from scrapers import get_scrapers
from utils.cv_parser import parse_cv
from routes.ai_routes import ai_routes # Import Blueprint
import os

app = Flask(__name__)

# Security: Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://" # In prod use Redis
)

# Security: Load secret from env or fallback for dev (change in prod!)
app.secret_key = os.getenv('SECRET_KEY', 'super-secret-key-change-this')

# Security: Limit upload size to 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

# Security: Cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_DEBUG', 'False').lower() != 'true' # Secure in Prod

csrf = CSRFProtect(app)

# Database Configuration - use env var or fallback to SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
default_db_uri = 'sqlite:///' + os.path.join(basedir, 'jobs.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', default_db_uri)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS Configuration - use env var or fallback to localhost
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:5174').split(',')
CORS(app, resources={r"/api/*": {"origins": cors_origins}}, supports_credentials=True)
db.init_app(app)

# Register Blueprints
app.register_blueprint(ai_routes, url_prefix='/api/ai')
from routes.admin_routes import admin_routes
app.register_blueprint(admin_routes, url_prefix='/api/admin')
from routes.seo_routes import seo_bp
app.register_blueprint(seo_bp, url_prefix='/') # Root for sitemap.xml

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/api/csrf-token', methods=['GET'])
def get_csrf_token():
    token = generate_csrf()
    response = jsonify({'csrf_token': token})
    # Ensure cookie is set if not already specific logic, though flask-wtf does this. 
    # Actually flask-wtf sets the token in the session or cookie. `generate_csrf()` ensures it.
    return response

# --- Auth Endpoints ---
# --- Auth Endpoints ---
@app.route('/api/auth/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
        
    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    login_user(user)
    return jsonify({'message': 'Registered successfully', 'user': user.to_dict()})

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'message': 'Logged in successfully', 'user': user.to_dict()})
        
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})

@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({'user': current_user.to_dict()})
    return jsonify({'user': None})

# --- Profile Endpoints ---
@app.route('/api/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    if request.method == 'GET':
        return jsonify(current_user.to_dict())
    
    data = request.json
    current_user.name = data.get('name', current_user.name)
    current_user.phone = data.get('phone', current_user.phone)
    current_user.summary = data.get('summary', current_user.summary)
    current_user.skills = data.get('skills', current_user.skills)
    current_user.experience = data.get('experience', current_user.experience)
    current_user.education = data.get('education', current_user.education)
    
    db.session.commit()
    return jsonify({'message': 'Profile updated', 'user': current_user.to_dict()})


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    query = request.args.get('q', '')
    location = request.args.get('location', '')
    
    # Basic filtering
    sql_query = Job.query
    if query:
        sql_query = sql_query.filter(Job.title.ilike(f'%{query}%'))
    if location:
        sql_query = sql_query.filter(Job.location.ilike(f'%{location}%'))
        
    jobs = sql_query.order_by(Job.date_posted.desc()).all()
    return jsonify([job.to_dict() for job in jobs])

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify(job.to_dict())

@app.route('/api/scrape', methods=['POST'])
def trigger_scrape():
    data = request.json
    query = data.get('q', 'developer')
    location = data.get('location', 'India')
    
    scrapers = get_scrapers()
    total_jobs_added = 0
    errors = []
    
    for scraper in scrapers:
        try:
            print(f"Running {scraper.__class__.__name__}...")
            jobs_data = scraper.scrape(query, location)
            for job_data in jobs_data:
                # Check for duplicates by URL
                existing = Job.query.filter_by(url=job_data['url']).first()
                if not existing:
                    new_job = Job(**job_data)
                    db.session.add(new_job)
                    total_jobs_added += 1
        except Exception as e:
            print(f"Scraper failed: {e}")
            errors.append(str(e))
            
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database commit failed', 'details': str(e)}), 500

    return jsonify({
        'message': f'Scraping completed. Added {total_jobs_added} new jobs.',
        'errors': errors
    })

@app.route('/api/parse-cv', methods=['POST'])
def parse_user_cv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part provided'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if file:
        # Read content for storage
        file_content = file.read()
        
        # Reset pointer for parsing
        file.seek(0)
        
        # Parse
        data = parse_cv(file, file.filename)
        
        # Save to DB if user is logged in
        if current_user.is_authenticated:
            try:
                current_user.resume_data = file_content
                current_user.resume_filename = file.filename
                current_user.resume_content_type = file.content_type
                db.session.commit()
                print(f"Saved resume {file.filename} to DB for user {current_user.email}")
            except Exception as e:
                print(f"Failed to save resume blob: {e}")
                db.session.rollback()
        
        return jsonify(data)
    
    return jsonify({'error': 'File upload failed'}), 400

# --- Saved Jobs Endpoints ---
@app.route('/api/user/saved-jobs/<int:job_id>', methods=['POST'])
@login_required
def toggle_saved_job(job_id):
    saved_job = SavedJob.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    if saved_job:
        db.session.delete(saved_job)
        message = 'Job removed from saved'
        is_saved = False
    else:
        saved_job = SavedJob(user_id=current_user.id, job_id=job_id)
        db.session.add(saved_job)
        message = 'Job saved'
        is_saved = True
    
    db.session.commit()
    return jsonify({'message': message, 'is_saved': is_saved})

@app.route('/api/user/saved-jobs', methods=['GET'])
@login_required
def get_saved_jobs():
    saved_jobs = SavedJob.query.filter_by(user_id=current_user.id).all()
    # Return full job details
    return jsonify([sj.job.to_dict() for sj in saved_jobs])

@app.route('/api/user/saved-jobs/ids', methods=['GET'])
@login_required
def get_saved_job_ids():
    saved_jobs = SavedJob.query.filter_by(user_id=current_user.id).all()
    return jsonify([sj.job_id for sj in saved_jobs])

# --- Application Tracker Endpoints ---
@app.route('/api/user/applications', methods=['GET', 'POST'])
@login_required
def user_applications():
    if request.method == 'GET':
        apps = Application.query.filter_by(user_id=current_user.id).order_by(Application.date_applied.desc()).all()
        return jsonify([app.to_dict() for app in apps])
    
    data = request.json
    new_app = Application(
        user_id=current_user.id,
        company=data.get('company'),
        title=data.get('title'),
        status=data.get('status', 'Applied'),
        notes=data.get('notes', ''),
        job_id=data.get('job_id') 
    )
    db.session.add(new_app)
    db.session.commit()
    return jsonify({'message': 'Application added', 'application': new_app.to_dict()})

@app.route('/api/user/applications/<int:app_id>', methods=['PUT', 'DELETE'])
@login_required
def manage_application(app_id):
    app_entry = Application.query.get_or_404(app_id)
    if app_entry.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    if request.method == 'DELETE':
        db.session.delete(app_entry)
        db.session.commit()
        return jsonify({'message': 'Application deleted'})
        
    data = request.json
    app_entry.company = data.get('company', app_entry.company)
    app_entry.title = data.get('title', app_entry.title)
    app_entry.status = data.get('status', app_entry.status)
    app_entry.notes = data.get('notes', app_entry.notes)
    
    db.session.commit()
    return jsonify({'message': 'Application updated', 'application': app_entry.to_dict()})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    print("\n\n--- REGISTERED ROUTES ---\n")
    print(app.url_map)
    print("\n-------------------------\n\n")

    # Security: Disable debug in production
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, port=5000, host='0.0.0.0')
