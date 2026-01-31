from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db, User, Job, Application
from functools import wraps

admin_routes = Blueprint('admin_routes', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_routes.route('/stats', methods=['GET'])
@login_required
@admin_required
def get_stats():
    user_count = User.query.count()
    job_count = Job.query.count()
    app_count = Application.query.count()
    
    return jsonify({
        'users': user_count,
        'jobs': job_count,
        'applications': app_count
    })

@admin_routes.route('/users', methods=['GET'])
@login_required
@admin_required
def get_users():
    users = User.query.all()
    # Exclude detailed resume data for privacy/performance
    return jsonify([{
        'id': u.id,
        'email': u.email,
        'name': u.name,
        'is_admin': u.is_admin,
        'has_resume': u.resume_data is not None
    } for u in users])

@admin_routes.route('/jobs', methods=['POST'])
@login_required
@admin_required
def create_job():
    data = request.json
    try:
        new_job = Job(
            title=data['title'],
            company=data['company'],
            location=data['location'],
            source='Manual',
            url=data.get('url', f"manual-{int(datetime.utcnow().timestamp())}"), # simple unique url
            description=data.get('description', '')
        )
        db.session.add(new_job)
        db.session.commit()
        return jsonify({'message': 'Job created', 'job': new_job.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@admin_routes.route('/jobs/<int:job_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message': 'Job deleted'})

@admin_routes.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    if user.is_admin:
         return jsonify({'error': 'Cannot delete admin users'}), 403

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

@admin_routes.route('/scraper/run', methods=['POST'])
@login_required
@admin_required
def run_scraper():
    data = request.json or {}
    query = data.get('q', 'developer')
    location = data.get('location', 'India')
    
    from scrapers import get_scrapers
    scrapers = get_scrapers()
    total_added = 0
    errors = []
    
    for scraper in scrapers:
        try:
            jobs_data = scraper.scrape(query, location)
            for job_data in jobs_data:
                existing = Job.query.filter_by(url=job_data['url']).first()
                if not existing:
                    new_job = Job(**job_data)
                    db.session.add(new_job)
                    total_added += 1
        except Exception as e:
            errors.append(str(e))
            
    db.session.commit()
    return jsonify({'message': f'Scraping finished. Added {total_added} jobs.', 'errors': errors})

from datetime import datetime
