import pytest
import sys
import os

# Add backend to path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app, db, User

@pytest.fixture
def test_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Create tables
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()

@pytest.fixture
def db_session(test_app):
    with app.app_context():
        yield db.session
        db.session.rollback()

@pytest.fixture
def auth_headers(client):
    """Register and login a user, return headers"""
    email = "test@example.com"
    password = "password"
    
    # Register
    client.post('/api/auth/register', json={
        'email': email,
        'password': password,
        'name': 'Test User'
    })
    
    # Login
    resp = client.post('/api/auth/login', json={
        'email': email,
        'password': password
    })
    
    # Return cookies/headers if needed, but Flask test client handles cookies automatically
    # We just need to ensure we are logged in.
    return resp

@pytest.fixture
def admin_headers(client, test_app):
    """Register and login an ADMIN user"""
    email = "admin@example.com"
    password = "password"
    
    # Register manually to set is_admin
    with test_app.app_context():
        user = User(email=email, name="Admin User", is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
    # Login
    client.post('/api/auth/login', json={
        'email': email,
        'password': password
    })
    
    return client
