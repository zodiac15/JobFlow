from flask import Blueprint, Response, url_for
from models import Job
from datetime import datetime

seo_bp = Blueprint('seo', __name__)

@seo_bp.route('/sitemap.xml')
def sitemap():
    """Generates a Sitemap XML for all jobs."""
    jobs = Job.query.all()
    base_url = "http://localhost:5173" # Frontend URL
    
    xml = []
    xml.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Static pages
    for route in ['/', '/login', '/register']:
        xml.append('<url>')
        xml.append(f'<loc>{base_url}{route}</loc>')
        xml.append('<changefreq>weekly</changefreq>')
        xml.append('</url>')

    # Dynamic Job Pages
    for job in jobs:
        xml.append('<url>')
        xml.append(f'<loc>{base_url}/job/{job.id}</loc>')
        # Convert datetime to YYYY-MM-DD
        date_str = job.date_posted.strftime('%Y-%m-%d') if job.date_posted else datetime.now().strftime('%Y-%m-%d')
        xml.append(f'<lastmod>{date_str}</lastmod>')
        xml.append('<changefreq>daily</changefreq>')
        xml.append('</url>')
        
    xml.append('</urlset>')
    
    return Response('\n'.join(xml), mimetype='application/xml')
