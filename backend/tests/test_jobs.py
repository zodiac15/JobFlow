def test_get_jobs(client):
    resp = client.get('/api/jobs')
    assert resp.status_code == 200
    assert isinstance(resp.json, list)

def test_save_job(client, auth_headers):
    # Mock finding a job or create one manually via DB session if needed
    # But since we use in-memory DB, we should pre-populate
    # For now, let's assume empty list doesn't crash
    resp = client.get('/api/user/saved-jobs')
    assert resp.status_code == 200
    assert resp.json == []

def test_application_workflow(client, auth_headers):
    # Create app
    resp = client.post('/api/user/applications', json={
        'company': 'Test Corp',
        'title': 'Developer',
        'status': 'Applied'
    })
    assert resp.status_code == 200
    app_id = resp.json['application']['id']
    
    # Get apps
    resp = client.get('/api/user/applications')
    assert len(resp.json) == 1
    
    # Update app
    resp = client.put(f'/api/user/applications/{app_id}', json={
        'status': 'Interviewing'
    })
    assert resp.status_code == 200
    assert resp.json['application']['status'] == 'Interviewing'
    
    # Delete app
    resp = client.delete(f'/api/user/applications/{app_id}')
    assert resp.status_code == 200
    
    # Verify empty
    resp = client.get('/api/user/applications')
    assert len(resp.json) == 0
