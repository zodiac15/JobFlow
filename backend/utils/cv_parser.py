import re
from pypdf import PdfReader
from docx import Document

def extract_text_from_pdf(file_stream):
    try:
        reader = PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def extract_text_from_docx(file_stream):
    try:
        doc = Document(file_stream)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return ""

def parse_cv(file_stream, filename):
    text = ""
    if filename.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_stream)
    elif filename.lower().endswith('.docx'):
        text = extract_text_from_docx(file_stream)
    else:
        return {'error': 'Unsupported file format'}

    # Try Gemini Parsing First
    from utils.gemini_client import generate_json_content, GEMINI_API_KEY
    
    if GEMINI_API_KEY:
        print("Using Gemini for CV Parsing...")
        prompt = f"""
        You are an expert Resume Parser. Extract the following information from the resume text below and return it in JSON format:
        
        Resume Text:
        {text[:30000]} 

        Required JSON Structure:
        {{
            "name": "Candidate Name",
            "email": "email@example.com",
            "phone": "123-456-7890",
            "summary": "Professional summary...",
            "skills": ["Skill1", "Skill2"],
            "education": [
                {{ "school": "University Name", "degree": "Degree Name", "year": "2020" }}
            ],
            "experience": [
                {{ "company": "Company Name", "role": "Job Title", "duration": "Dates", "description": "Brief description" }}
            ],
            "links": ["linkedin.com/in/...", "github.com/..."]
        }}
        
        If a field is missing, use empty string or empty list.
        """
        
        gemini_result = generate_json_content(prompt)
        if gemini_result:
             # Basic validation
             if 'name' in gemini_result:
                 return gemini_result
    
    # Fallback to Regex
    print("Fallback to Regex Parsing...")
    return extract_info_advanced(text)

def extract_info_advanced(text):
    info = {
        'name': '',
        'email': '',
        'phone': '',
        'skills': [],
        'summary': '',
        'links': [],
        'education': [],
        'experience': []
    }
    
    # Pre-processing
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        return info

    # 1. Basic Info (Header Extraction - usually top 10 lines)
    header_lines = lines[:15]
    header_text = "\n".join(header_lines)
    
    # Email
    email_regex = r'[\w\.-]+@[\w\.-]+\.\w+'
    email_match = re.search(email_regex, header_text)
    if email_match:
        info['email'] = email_match.group(0)

    # Phone
    phone_regex = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phone_match = re.search(phone_regex, header_text)
    if phone_match:
        info['phone'] = phone_match.group(0)
    
    # Name
    # Heuristic: First line that isn't a known header or mostly numbers
    for line in header_lines:
        if len(line) < 50 and not re.search(r'\d', line) and '@' not in line:
            info['name'] = line
            break
            
    # Links
    link_regex = r'(https?://(?:www\.)?(?:linkedin\.com|github\.com)[^\s]*)'
    links = re.findall(link_regex, text)
    info['links'] = list(set(links))

    # 2. Section Segmentation
    sections = segment_sections(lines)
    
    # 3. Process Sections
    if 'skills' in sections:
        info['skills'] = extract_skills(sections['skills'])
    else:
        # Fallback: Scan whole text if no skills section found
        info['skills'] = extract_skills(lines)
        
    if 'education' in sections:
        info['education'] = extract_education(sections['education'])
        
    if 'experience' in sections:
        info['experience'] = extract_experience(sections['experience'])
    
    # Summary is often the intro before proper sections
    if 'summary' in sections:
         info['summary'] = " ".join(sections['summary'][:3]) # First few lines
    elif len(header_lines) > 2:
         # Fallback heuristic
         for line in header_lines:
             if len(line) > 50 and '@' not in line:
                 info['summary'] = line
                 break

    return info

def segment_sections(lines):
    sections = {}
    current_section = None
    
    # Regex for headers
    headers = {
        'experience': r'(?i)^(experience|work history|employment history|professional experience)',
        'education': r'(?i)^(education|academic background|qualifications)',
        'skills': r'(?i)^(skills|technical skills|technologies|core competencies)',
        'projects': r'(?i)^(projects|personal projects)',
        'summary': r'(?i)^(summary|profile|about me|professional summary)'
    }
    
    for line in lines:
        is_header = False
        for key, regex in headers.items():
            if re.match(regex, line):
                current_section = key
                sections[key] = []
                is_header = True
                break
        
        if not is_header and current_section:
            sections[current_section].append(line)
            
    return sections

def extract_skills(lines):
    tech_skills = [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
        'html', 'css', 'react', 'vue', 'angular', 'node', 'flask', 'django',
        'sql', 'nosql', 'aws', 'azure', 'docker', 'kubernetes', 'git',
        'machine learning', 'ai', 'data analysis', 'selenium', 'pandas', 'numpy',
        'powershell', 'active directory', 'servicenow', 'system engineer', 'identity management'
    ]
    
    found_skills = set()
    text = " ".join(lines).lower()
    
    for skill in tech_skills:
        if skill in text:
            found_skills.add(skill.title())
            
    return list(found_skills)

def extract_education(lines):
    entries = []
    for line in lines:
        if any(w in line.lower() for w in ['university', 'college', 'bachelor', 'master', 'degree', 'b.tech', 'm.tech']):
             entries.append({'school': line, 'degree': '', 'year': ''})
    return entries

def extract_experience(lines):
    entries = []
    current_entry = None
    
    # Regex for dates: e.g. "2020 - 2021", "Jan 2020 - Present", "October 2023 - Present"
    date_regex = r'(?i)((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}|\d{4})\s*[-–]\s*(present|current|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}|\d{4})'
    
    for line in lines:
        date_match = re.search(date_regex, line)
        if date_match:
            if current_entry:
                entries.append(current_entry)
            
            # Line typically: "Company | Role Date" or "Company - Role Date" or "Role | Company"
            # Remove the date part for analysis
            raw_header = line.replace(date_match.group(0), '').strip()
            
            role = raw_header
            company = ''
            
            # Splitters: | or - or ,
            if '|' in raw_header:
                parts = raw_header.split('|')
                company = parts[0].strip()
                role = parts[1].strip() if len(parts) > 1 else ''
            elif ' - ' in raw_header: # Be careful with hyphen in names
                parts = raw_header.split(' - ')
                company = parts[0].strip()
                role = parts[1].strip() if len(parts) > 1 else ''
            
            current_entry = {
                'role': role,
                'company': company,
                'duration': date_match.group(0)
            }
        elif current_entry:
            # If we didn't find a company in the header, try looking here
            if not current_entry['company'] and not current_entry['role']:
                 # Maybe the header line was Just Date? Unlikely with this regex.
                 pass
            
            # Heuristic: If we haven't found a company yet, and this line looks like one?
            # For ayush.pdf, the format was "Company | Role Date". So we handled it above.
            pass
            
    if current_entry:
        entries.append(current_entry)
        
    return entries
