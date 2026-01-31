from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

ai_routes = Blueprint('ai_routes', __name__)

@ai_routes.route('/generate-resume', methods=['POST'])
@login_required
def generate_resume():
    data = request.json
    job_description = data.get('job_description')
    base_resume = data.get('base_resume') # Can be text or JSON
    
    if not job_description or not base_resume:
        return jsonify({'error': 'Missing job description or base resume'}), 400
        
    from utils.gemini_client import generate_content, GEMINI_API_KEY
    
    if not GEMINI_API_KEY:
        return jsonify({'error': 'AI service not configured'}), 503

    user = current_user
    
    prompt = f"""
    You are an expert Resume Writer. Your task is to re-write and tailor the candidate's resume to perfectly match the provided Job Description.
    
    JOB DESCRIPTION:
    {job_description[:10000]}
    
    CANDIDATE'S BASE RESUME INFO:
    {base_resume}
    
    INSTRUCTIONS:
    1. Analyze the Job Description for keywords, skills, and requirements.
    2. Re-write the candidate's resume to highlight relevant experience and skills.
    3. Use professional Resume markdown format.
    4. Keep the same contact info as provided in the base resume.
    5. Do NOT invent false information, but emphasize the relevant truth.
    
    OUTPUT FORMAT:
    Return ONLY the Markdown content of the new resume.
    """
    
    generated_resume = generate_content(prompt)
    
    if not generated_resume:
        return jsonify({'error': 'Failed to generate resume'}), 500
        
    return jsonify({'resume': generated_resume})

