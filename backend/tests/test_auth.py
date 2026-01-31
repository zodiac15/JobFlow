def test_register(client):
    resp = client.post('/api/auth/register', json={
        'email': 'new@example.com',
        'password': 'pass',
        'name': 'New User'
    })
    assert resp.status_code == 200
    assert resp.json['message'] == 'Registered successfully'

def test_register_duplicate(client, auth_headers):
    # auth_headers creates test@example.com
    resp = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'pass',
        'name': 'Duplicate'
    })
    assert resp.status_code == 400
    assert 'already exists' in resp.json['error']

def test_login_success(client):
    # Create user first
    client.post('/api/auth/register', json={
        'email': 'login@example.com',
        'password': 'pass',
        'name': 'Login User'
    })
    
    resp = client.post('/api/auth/login', json={
        'email': 'login@example.com',
        'password': 'pass'
    })
    assert resp.status_code == 200
    assert resp.json['message'] == 'Logged in successfully'

def test_login_failure(client):
    resp = client.post('/api/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrong'
    })
    assert resp.status_code == 401

def test_logout(client, auth_headers):
    resp = client.post('/api/auth/logout')
    assert resp.status_code == 200
    
    # Verify unauthorized access after logout
    resp = client.get('/api/auth/me')
    assert resp.json['user'] is None
