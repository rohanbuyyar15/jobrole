import PyPDF2
from io import BytesIO
import re

def extract_text_from_pdf(file_stream):
    try:
        reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
        return text.strip()
    except Exception as e:
        return ""

def validate_resume(text):
    text_lower = text.lower()
    keywords = ["skills", "education", "experience", "projects", "work", "profile"]
    match_count = sum(1 for kw in keywords if kw in text_lower)
    return match_count >= 2

def clean_text(text):
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return text.lower()

# For benchmarking
ROLE_SKILLS = {
    "Data Scientist": ["python", "sql", "machine learning", "statistics", "pandas", "numpy", "data visualization"],
    "ML Engineer": ["python", "pytorch", "tensorflow", "nlp", "computer vision", "llm", "mlops", "docker"],
    "Web Developer": ["html", "css", "javascript", "react", "nodejs", "nextjs", "typescript", "tailwindcss"]
}

def analyze_gap(text, predicted_role):
    text_lower = text.lower()
    required = ROLE_SKILLS.get(predicted_role, [])
    
    found_skills = []
    missing_skills = []
    
    for skill in required:
        if skill in text_lower:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)
            
    match_score = int((len(found_skills) / max(1, len(required))) * 100)
    
    return match_score, missing_skills

def generate_roadmap(missing_skills, role):
    roadmap = []
    step = 1
    for skill in missing_skills:
        roadmap.append(f"Step {step}: Learn and practice {skill.title()}")
        step += 1
    
    if not roadmap:
        roadmap.append("Keep learning advanced topics in your field!")
        
    return roadmap

def generate_suggestions(text):
    text_lower = text.lower()
    suggestions = []
    
    if "github.com" not in text_lower:
        suggestions.append("Add a GitHub link to showcase your code.")
    if "linkedin.com" not in text_lower:
        suggestions.append("Add a LinkedIn profile link.")
    if "projects" not in text_lower:
        suggestions.append("Add a dedicated 'Projects' section to highlight practical work.")
    if "education" not in text_lower:
        suggestions.append("Ensure your Education history is clearly visible.")
        
    if not suggestions:
        suggestions.append("Your resume looks well-structured. Keep descriptions metric-driven!")
        
    return suggestions
