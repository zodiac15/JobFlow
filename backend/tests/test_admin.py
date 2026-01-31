def test_admin_access_denied(client, auth_headers):
    # Standard user trying to access admin stats
    resp = client.get('/api/admin/stats')
    assert resp.status_code == 403

def test_admin_access_granted(client, admin_headers):
    resp = client.get('/api/admin/stats')
    assert resp.status_code == 200
    data = resp.json
    assert 'users' in data
    assert 'jobs' in data

def test_admin_user_list(client, admin_headers):
    resp = client.get('/api/admin/users')
    assert resp.status_code == 200
    assert isinstance(resp.json, list)
    # Should see at least the admin user
    assert len(resp.json) >= 1

def test_create_and_delete_job(client, admin_headers):
    # Create
    resp = client.post('/api/admin/jobs', json={
        'title': 'Admin Job',
        'company': 'Admin Corp',
        'location': 'Remote'
    })
    assert resp.status_code == 200
    job_id = resp.json['job']['id']
    
    # Delete
    resp = client.delete(f'/api/admin/jobs/{job_id}')
    assert resp.status_code == 200
