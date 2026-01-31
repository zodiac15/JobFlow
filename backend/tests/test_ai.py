import pytest
from unittest.mock import patch, MagicMock

@patch('utils.gemini_client.generate_content')
def test_generate_resume_mocked(mock_generate, client, auth_headers):
    # Mock the Gemini response string directly
    mock_generate.return_value = """
    # John Doe
    ## Summary
    Tailored summary...
    """

    # We need a user profile for this to work, which auth_headers provides
    # Test generation
    resp = client.post('/api/ai/generate-resume', json={
        'job_description': 'Python Developer',
        'base_resume': 'John Doe...'
    })
    
    # We changed endpoint usage in test! The endpoint expects job_description and base_resume
    # OR job_id? Let's check ai_routes.py again.
    # ai_routes.py lines 9-11:
    # data = request.json
    # job_description = data.get('job_description')
    # base_resume = data.get('base_resume')
    
    assert resp.status_code == 200
    assert 'resume' in resp.json
    assert 'John Doe' in resp.json['resume']

def test_generate_resume_missing_data(client, auth_headers):
    resp = client.post('/api/ai/generate-resume', json={})
    assert resp.status_code == 400
    assert 'Missing' in resp.json['error']
    
def test_placeholder_ai(client):
    assert True
