import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

# NLP / ML imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

app = Flask(__name__)
# Enable CORS so the Vercel frontend can communicate with this backend
CORS(app)

# -----------------------------------
# GLOBAL ML STATE (Stateless)
# -----------------------------------

# 1. Define required skills for benchmarking and training data
ROLE_SKILLS = {
    "Frontend Developer": ["html", "css", "javascript", "react", "vue", "angular", "bootstrap", "tailwind", "ui", "ux", "responsive"],
    "Backend Developer": ["python", "java", "node", "express", "django", "flask", "sql", "api", "rest", "database", "mongodb", "postgresql", "docker"],
    "Data Scientist": ["python", "r", "sql", "machine learning", "deep learning", "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "statistics", "math"],
    "Full Stack Developer": ["html", "css", "javascript", "react", "node", "express", "python", "django", "sql", "mongodb", "api", "aws"],
    "DevOps Engineer": ["aws", "azure", "docker", "kubernetes", "jenkins", "cicd", "linux", "bash", "python", "terraform", "ansible"]
}

# 2. Stopwords basic list
STOPWORDS = set([
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", 
    "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", 
    "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", 
    "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", 
    "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", 
    "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", 
    "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", 
    "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", 
    "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", 
    "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", 
    "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", 
    "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
])

# Resume detection keywords (checking for keywords universally found in resumes)
RESUME_KEYWORDS = ["education", "experience", "skills", "projects", "summary", "objective", "certifications", "university", "degree", "college"]


# Initialize TF-IDF and Logistic Regression
vectorizer = TfidfVectorizer()
clf = LogisticRegression(probability=True, random_state=42)

def train_model():
    """
    Trains a simple Logistic Regression model on startup using dummy data.
    This fulfills the requirement of ML Model without using a Database.
    """
    documents = []
    labels = []
    
    # We expand the keywords into synthetic "resumes" 
    # to train our model simply
    for role, skills in ROLE_SKILLS.items():
        base_doc = " ".join(skills)
        documents.append(base_doc + " experience projects education skills")
        documents.append(" ".join(skills[:len(skills)//2]) + " worked as a " + role)
        documents.append(" ".join(skills[len(skills)//2:]) + " certified in " + role)
        labels.extend([role, role, role])
    
    X = vectorizer.fit_transform(documents)
    clf.fit(X, labels)

# Train the model memory on startup
train_model()

# -----------------------------------
# HELPER FUNCTIONS
# -----------------------------------

def preprocess_text(text):
    """
    NLP PROCESSING:
    - Convert text to lowercase
    - Remove punctuation
    - Remove stopwords
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in STOPWORDS]
    return " ".join(tokens)

def is_resume(text):
    """
    INPUT VALIDATION:
    Check if input is a resume using keyword-based logic.
    Requires at least 2 common resume keywords to be considered a valid resume.
    """
    text_lower = text.lower()
    matches = sum(1 for kw in RESUME_KEYWORDS if kw in text_lower)
    return matches >= 2

def predict_roles(processed_text):
    """
    JOB ROLE PREDICTION:
    Predict top 3 roles with confidence %
    """
    X_input = vectorizer.transform([processed_text])
    probabilities = clf.predict_proba(X_input)[0]
    
    # Get indices of top 3 probabilities
    top_indices = np.argsort(probabilities)[::-1][:3]
    
    results = []
    for idx in top_indices:
        role = clf.classes_[idx]
        confidence = probabilities[idx] * 100
        results.append({
            "role": role,
            "confidence": round(confidence, 2)
        })
    return results

def benchmark_and_gap_analysis(text_lower, predicted_role):
    """
    BENCHMARKING & GAP ANALYSIS:
    Compare with required skills, calculate match score, and identify missing skills.
    """
    required_skills = ROLE_SKILLS.get(predicted_role, [])
    found_skills = []
    missing_skills = []
    
    for skill in required_skills:
        # Simple string match for skills
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.append(skill)
        else:
            missing_skills.append(skill)
            
    # Calculate match score based on percentage of found required skills
    if not required_skills:
        match_score = 0
    else:
        match_score = len(found_skills) / len(required_skills) * 100
        
    return round(match_score, 2), missing_skills

def generate_roadmap_and_suggestions(missing_skills, match_score):
    """
    ROADMAP GENERATION & RESUME SUGGESTIONS:
    Create actionable steps to improve based on missing skills.
    """
    roadmap = []
    suggestions = []
    
    if match_score < 50:
        suggestions.append("Your resume lacks keywords matching the top predicted role. Tailor your resume more carefully towards your desired role.")
    elif match_score < 80:
        suggestions.append("Good start, but you could highlight more relevant skills to improve your chances.")
    else:
        suggestions.append("Great resume! Your skills strongly match the target role.")
        
    if missing_skills:
        suggestions.append(f"Consider adding experiences that demonstrate your abilities in: {', '.join(missing_skills[:3])}.")
        
        roadmap.append("Step 1: Focus on learning the core missing skills: " + ", ".join(missing_skills[:3]) + ".")
        roadmap.append("Step 2: Build a small project utilizing these new skills to demonstrate practical application.")
        roadmap.append("Step 3: Update your resume's 'Skills' and 'Projects' sections to include them in action.")
    else:
        roadmap.append("Keep your skills up to date with the latest industry standards.")
        roadmap.append("Focus on advanced concepts and seeking out leadership roles or architecture design.")
        
    return roadmap, suggestions

def analyze_sections(text_lower):
    """
    SECTION ANALYSIS:
    Detect Skills, Projects, Experience sections and mark as Strong/Weak/Missing
    """
    sections = {
        "Experience": {"keywords": ["experience", "work history", "employment", "history"], "found": False, "length": 0},
        "Projects": {"keywords": ["projects", "personal projects", "academic projects"], "found": False, "length": 0},
        "Skills": {"keywords": ["skills", "technical skills", "core competencies"], "found": False, "length": 0}
    }
    
    results = {}
    
    for sec_name, meta in sections.items():
        # Heuristic check
        for kw in meta["keywords"]:
            idx = text_lower.find(kw)
            if idx != -1:
                meta["found"] = True
                # Get a rough estimate of the section length by grabbing substring to the end or next ~100 words
                vicinity = text_lower[idx:idx+500]
                meta["length"] = len(vicinity.split())
                break
                
        if not meta["found"]:
            results[sec_name] = "Missing"
        elif meta["length"] < 20:
            results[sec_name] = "Weak"
        else:
            results[sec_name] = "Strong"
            
    return results

# -----------------------------------
# ROUTES
# -----------------------------------

@app.route('/')
def index():
    return jsonify({"status": "Backend running successfully!"})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    resume_text = data.get('resume', '').strip()
    
    if not resume_text:
        return jsonify({"error": "Empty input."}), 400
        
    # 1. Input Validation
    if not is_resume(resume_text):
        # Specific rejection message
        return jsonify({"error": "Invalid Input – Not a Resume"})
        
    # 2. NLP Processing
    processed_text = preprocess_text(resume_text)
    
    # 3. Job Role Prediction
    predictions = predict_roles(processed_text)
    primary_role = predictions[0]['role']
    
    # 4 & 5. Benchmarking and Gap Analysis
    text_lower = resume_text.lower()
    match_score, missing_skills = benchmark_and_gap_analysis(text_lower, primary_role)
    
    # 6 & 7. Roadmap Generation & Resume Suggestions
    roadmap, suggestions = generate_roadmap_and_suggestions(missing_skills, match_score)
    
    # 8. Section Analysis
    section_grades = analyze_sections(text_lower)
    
    # 10. Output Formatting (returned as JSON, handled cleanly via the frontend)
    response = {
        "predictions": predictions,
        "match_score": match_score,
        "missing_skills": missing_skills,
        "roadmap": roadmap,
        "suggestions": suggestions,
        "sections": section_grades
    }
    
    return jsonify(response)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
