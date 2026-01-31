from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    summary = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Storing complex data as JSON strings for simplicity in SQLite
    _skills = db.Column('skills', db.Text, default='[]')
    _experience = db.Column('experience', db.Text, default='[]')
    _education = db.Column('education', db.Text, default='[]')

    # Resume Storage
    resume_data = db.Column(db.LargeBinary) # BLOB for file content
    resume_filename = db.Column(db.String(255))
    resume_content_type = db.Column(db.String(50))

    @property
    def skills(self):
        return json.loads(self._skills)
    
    @skills.setter
    def skills(self, value):
        self._skills = json.dumps(value)

    @property
    def experience(self):
        return json.loads(self._experience)
    
    @experience.setter
    def experience(self, value):
        self._experience = json.dumps(value)

    @property
    def education(self):
        return json.loads(self._education)
    
    @education.setter
    def education(self, value):
        self._education = json.dumps(value)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'summary': self.summary,
            'skills': self.skills,
            'experience': self.experience,
            'education': self.education
        }

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(50), nullable=False)  # e.g., 'linkedin', 'naukri'
    url = db.Column(db.String(500), nullable=False, unique=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'source': self.source,
            'url': self.url,
            'date_posted': self.date_posted.isoformat(),
            'description': self.description
        }

class SavedJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    date_saved = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('saved_jobs', lazy=True))
    job = db.relationship('Job', backref=db.backref('saved_by_users', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'job': self.job.to_dict(),
            'date_saved': self.date_saved.isoformat()
        }

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Ideally link to a Job, but job might be external or deleted, so we cache basic info
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=True) 
    company = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='Applied') # Applied, Interviewing, Offer, Rejected
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    user = db.relationship('User', backref=db.backref('applications', lazy=True))
    job = db.relationship('Job', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'company': self.company,
            'title': self.title,
            'status': self.status,
            'date_applied': self.date_applied.isoformat(),
            'notes': self.notes
        }
